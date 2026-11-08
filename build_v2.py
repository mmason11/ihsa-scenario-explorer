"""
Build v2 dataset:
- keep the 9 requested spreadsheet sports
- add FLGG/LAXB/LAXG/VBB/WPB/WPG with actual IHSA sectional assignments
- add FB (playoff qualifiers by class)
- match IHSA-printed names to the master roster (coords + private status);
  geocode unmatched by city and flag them
Outputs: schools_data.json (consumed by build_site.py), match_report.txt
"""
import json, re, unicodedata
import pandas as pd
import zipcodes
from new_sports import ASSIGNMENTS, FOOTBALL

KEEP = ["SOB","SOG","VBG","BKB","BKG","CHC","DAC","BA","SBG"]

df = pd.read_csv("schools_master.csv")

def norm(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii","ignore").decode()
    s = s.lower().replace("[coop]","")
    s = re.sub(r"\[.*?\]","",s)                       # coop tags
    s = re.sub(r"\b([a-z])\.\-","",s)                 # "c.-monee" -> "monee"
    s = re.sub(r"\b([a-z])\. ","",s)                  # "w. warrenville" -> "warrenville"
    s = re.sub(r"[^a-z0-9()]+","",s)
    return s

master_by_norm = {}
for _, r in df.iterrows():
    master_by_norm.setdefault(norm(r.school), r.school)

def city_of(name):
    m = re.match(r"^([^(\[]+?)\s*[\(\[]", name)
    return (m.group(1) if m else name).strip()

def geocode(city):
    fixes = {"DuQuoin":"Du Quoin","Mt. Sterling":"Mount Sterling","Mt. Carmel":"Mount Carmel",
             "Mt. Zion":"Mt Zion","St. Joseph":"Saint Joseph","El Paso":"El Paso","Downs":"Downs"}
    city = fixes.get(city, city)
    for c in (city, city.replace("St.","Saint"), city.replace("Mt.","Mount")):
        res = [r for r in zipcodes.filter_by(city=c, state="IL") if r.get("lat")]
        if res:
            return (sum(float(r["lat"]) for r in res)/len(res),
                    sum(float(r["long"]) for r in res)/len(res))
    return None, None

# ---- resolve every ihsa-printed name to a record
extra_rows = []      # schools not in master
resolved = {}        # printed name -> canonical school name
report = []

def resolve(printed):
    if printed in resolved:
        return resolved[printed]
    clean = re.sub(r"\s*\[.*?\]\s*","",printed).strip()
    n = norm(clean)
    if n in master_by_norm:
        resolved[printed] = master_by_norm[n]
        return resolved[printed]
    # try dropping the paren detail: "Greenfield" etc.
    base = re.sub(r"\s*\(.*?\)\s*","",clean).strip()
    nb = norm(base)
    if nb in master_by_norm:
        resolved[printed] = master_by_norm[nb]
        report.append(f"LOOSE  {printed} -> {master_by_norm[nb]}")
        return resolved[printed]
    # unmatched: geocode by city, add as new record (assume public unless obviously not)
    city = city_of(clean)
    lat, lon = geocode(city)
    rec = {"school": clean, "city": city, "status": "unmatched", "is_private": False,
           "needs_review": True, "lat": lat, "lon": lon}
    extra_rows.append(rec)
    resolved[printed] = clean
    report.append(f"NEW    {printed} (geocoded {city}: {lat},{lon})")
    return clean

# base records
recs = {}
for _, r in df.iterrows():
    if pd.isna(r.lat):
        continue
    recs[r.school] = {"n": r.school, "la": round(r.lat,4), "lo": round(r.lon,4),
                      "p": 1 if r.is_private else 0, "st": r.status, "c": {},
                      "en": (round(r.enrollment,1) if pd.notna(r.enrollment) else None)}
    for s in KEEP:
        v = r[s]
        if isinstance(v,str) and v.strip():
            recs[r.school]["c"][s] = v.strip()

# new sports: assignments. Single-class sports are a flat list of
# (sectional_name, schools); multi-class sports (e.g. SOB) are a dict of
# class -> that same flat-list shape, since each class has its own independent
# set of sectionals.
def build_sectionals(secs):
    out = []
    for sec_name, schools in secs:
        canon = [resolve(s) for s in schools]
        out.append({"name": sec_name, "schools": canon})
    return out

assign_out = {}
for sport, secs in ASSIGNMENTS.items():
    if isinstance(secs, dict):
        assign_out[sport] = {kl: build_sectionals(class_secs) for kl, class_secs in secs.items()}
    else:
        assign_out[sport] = build_sectionals(secs)

# football classes
for kl, schools in FOOTBALL.items():
    for s in schools:
        resolve(s)

# add extra rows to recs
for e in extra_rows:
    if e["lat"] is None:
        report.append(f"NOGEO  {e['school']}")
        continue
    recs[e["school"]] = {"n": e["school"], "la": round(e["lat"],4), "lo": round(e["lon"],4),
                         "p": 0, "st": "unmatched", "c": {}, "en": None}

# stamp class values — only for single-class sports ("S" IS the class). Multi-class
# sports keep whatever real class came from the KEEP columns above; don't clobber it.
for sport, secs in assign_out.items():
    if isinstance(secs, dict):
        continue
    for sec in secs:
        for s in sec["schools"]:
            if s in recs:
                recs[s]["c"][sport] = "S"
for kl, schools in FOOTBALL.items():
    for s in schools:
        c = resolved[s]
        if c in recs:
            recs[c]["c"]["FB"] = kl

# state final-4 history (see pull_state_finalists.py), embedded per school as
# {sport: [years appeared]} — only sports/schools with at least one appearance, kept
# small since template.html computes the rolling-3-year success-factor window from
# this at runtime rather than baking in a specific year's window here.
try:
    with open("state_finalists.json", encoding="utf-8") as f:
        state_finalists = json.load(f)
except FileNotFoundError:
    state_finalists = {}
for sport, years in state_finalists.items():
    for year, teams in years.items():
        for team in teams:
            if team in recs:
                recs[team].setdefault("fin", {}).setdefault(sport, []).append(year)

# official classification flags (co-op/waiver/multiplier/success/playup) — see
# pull_classifications.py. Authoritative for SOB/VBG/BKB/BKG (fall+winter cycle pages
# only; no spring page found for BA/SBG/SOG as of this writing). Corrects our own
# class value where it differs — the official page reflects co-op combined enrollment
# schools_master.csv's per-school column can't — and records the flag for the Schools
# tab. Deliberately excludes CHC/DAC even though the source pages cover them: those
# use a different class-label scheme (S/M/L/C) than what's already in our data (see
# new_sports.py's docstring), and reconciling that is a separate task.
CLASS_FLAG_SPORTS = {"SOB", "VBG", "BKB", "BKG"}
try:
    with open("classifications_flags.json", encoding="utf-8") as f:
        class_flags = json.load(f)
except FileNotFoundError:
    class_flags = {}
flag_corrections = 0
for printed, sports in class_flags.items():
    n = norm(printed)
    canon = master_by_norm.get(n)
    if not canon or canon not in recs:
        continue
    for sport, d in sports.items():
        if sport not in CLASS_FLAG_SPORTS:
            continue
        if recs[canon]["c"].get(sport) != d["class"]:
            flag_corrections += 1
        recs[canon]["c"][sport] = d["class"]
        if d["flag"]:
            recs[canon].setdefault("flg", {})[sport] = d["flag"]
print(f"classification corrections applied (schools_master.csv value -> official): {flag_corrections}")

# MaxPreps team-strength ratings (see pull_maxpreps_rankings.py) — embedded per school
# as {sport: rating}, flattened from the richer per-class rank/record/rating/strength
# in maxpreps_ratings.json since a school's class is already known via its own "c"
# entry. Names in that file are already canonicalized against schools_data.json by
# the pull script itself, so no norm/match step is needed here (unlike
# classifications_flags.json above, which is keyed by IHSA-printed names). Water polo
# and girls flag football aren't covered — no usable MaxPreps rankings found for
# either (see pull_maxpreps_rankings.py's docstring).
try:
    with open("maxpreps_ratings.json", encoding="utf-8") as f:
        maxpreps_ratings = json.load(f)
except FileNotFoundError:
    maxpreps_ratings = {}
for sport, classes in maxpreps_ratings.items():
    for class_label, schools in classes.items():
        for school, d in schools.items():
            if school in recs:
                recs[school].setdefault("rtg", {})[sport] = d["rating"]

# Real 2025-26 season brackets (see pull_brackets.py) — actual seeds/scores/rounds
# per sectional, sourced straight from ihsa.org's own bracket pages rather than our
# synthetic MaxPreps reseed. Embedded as its own top-level key (like "assign") so
# template.html can render the Current side of the Bracket tab from real history;
# the Proposed side stays synthetic by design (it's inherently hypothetical).
try:
    with open("real_brackets.json", encoding="utf-8") as f:
        real_brackets = json.load(f)
except FileNotFoundError:
    real_brackets = {}

# Official IHSA non-boundaried schools list (source_data/Non-Boundaried_Schools.xlsx,
# sheets "Full Members" + "Approved Schools" — the list behind the Competitive Balance
# Committee's plan to give non-boundaried schools their own bracket quadrant). Embedded
# per school as nb:1; this is the separation basis for the committee plan in the UI.
# A private school missing from the list keeps nb:1 anyway (every IHSA private school
# is by definition non-boundaried; absence usually means a membership lapse — reported
# below rather than silently dropped). A school on the list that we had recorded as
# boundaried public gets its status corrected to public_nonboundaried (the official
# list wins over our earlier research).
nb_src = "source_data/Non-Boundaried_Schools.xlsx"
nb_names = []
for sheet in ("Full Members", "Approved Schools"):
    nb_df = pd.read_excel(nb_src, sheet_name=sheet)
    nb_names += [str(x).strip() for x in nb_df["NameIHSA"].dropna()]
recs_by_norm = {norm(k): k for k in recs}
nb_matched, nb_unmatched = set(), []
for printed in nb_names:
    k = norm(printed)
    if k in recs_by_norm:
        nb_matched.add(recs_by_norm[k])
    else:
        nb_unmatched.append(printed)
status_fixed = 0
for name, rec in recs.items():
    on_list = name in nb_matched
    rec["nb"] = 1 if (on_list or rec["p"] == 1) else 0
    if on_list and rec["st"] == "public":
        rec["st"] = "public_nonboundaried"
        status_fixed += 1
        report.append(f"NBFIX  {name}: status public -> public_nonboundaried (official NB list)")
    if rec["p"] == 1 and not on_list:
        report.append(f"NBGAP  {name}: private but not on official NB list (membership lapse?)")
for printed in nb_unmatched:
    report.append(f"NBMISS {printed}: on official NB list, fields no tracked sport (no record)")
print(f"non-boundaried: {len(nb_names)} official names, {len(nb_matched)} matched, "
      f"{len(nb_unmatched)} field no tracked sport | status fixes: {status_fixed} | "
      f"nb-flagged records: {sum(1 for r in recs.values() if r['nb'])}")

schools_out = list(recs.values())
with open("schools_data.json","w",encoding="utf-8",newline="\n") as f:
    f.write('{\n"schools": [\n')
    for i, s in enumerate(schools_out):
        line = json.dumps(s, separators=(",",":"), ensure_ascii=False)
        f.write(line + (",\n" if i < len(schools_out)-1 else "\n"))
    f.write('],\n"assign": ')
    f.write(json.dumps(assign_out, indent=1, ensure_ascii=False))
    f.write(',\n"brk": ')
    f.write(json.dumps(real_brackets, indent=1, ensure_ascii=False))
    f.write("\n}\n")

with open("match_report.txt","w",encoding="utf-8") as f:
    f.write("\n".join(report))

n_new = len([r for r in report if r.startswith("NEW")])
print(f"schools: {len(recs)} | new sport records added: {n_new} | loose matches: "
      f"{len([r for r in report if r.startswith('LOOSE')])}")
print(f"no-geocode failures: {len([r for r in report if r.startswith('NOGEO')])}")
for line in report[:40]:
    print(" ", line)
