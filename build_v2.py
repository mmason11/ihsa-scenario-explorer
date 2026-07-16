"""
Build v2 dataset:
- keep the 9 requested spreadsheet sports
- add FLGG/LAXB/LAXG/VBB/WPB/WPG with actual IHSA sectional assignments
- add FB (playoff qualifiers by class)
- match IHSA-printed names to the master roster (coords + private status);
  geocode unmatched by city and flag them
Outputs: schools_data_v2.json (for the explorer), match_report.txt
"""
import json, re, unicodedata
import pandas as pd
import zipcodes
from new_sports import ASSIGNMENTS, FOOTBALL

KEEP = ["SOB","SOG","VBG","BKB","BKG","CHC","DAC","BA","SBG"]

df = pd.read_csv("/home/claude/ihsa/schools_master.csv")

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
                      "p": 1 if r.is_private else 0, "st": r.status, "c": {}}
    for s in KEEP:
        v = r[s]
        if isinstance(v,str) and v.strip():
            recs[r.school]["c"][s] = v.strip()

# new sports: assignments
assign_out = {}
for sport, secs in ASSIGNMENTS.items():
    assign_out[sport] = []
    for sec_name, schools in secs:
        canon = []
        for s in schools:
            c = resolve(s)
            canon.append(c)
        assign_out[sport].append({"name": sec_name, "schools": canon})

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
                         "p": 0, "st": "unmatched", "c": {}}

# stamp class values
for sport, secs in assign_out.items():
    for sec in secs:
        for s in sec["schools"]:
            if s in recs:
                recs[s]["c"][sport] = "S"
for kl, schools in FOOTBALL.items():
    for s in schools:
        c = resolved[s]
        if c in recs:
            recs[c]["c"]["FB"] = kl

out = {"schools": list(recs.values()), "assign": assign_out}
with open("/home/claude/ihsa/schools_data_v2.json","w") as f:
    json.dump(out, f, separators=(",",":"), ensure_ascii=False)

with open("/home/claude/ihsa/match_report.txt","w") as f:
    f.write("\n".join(report))

n_new = len([r for r in report if r.startswith("NEW")])
print(f"schools: {len(recs)} | new sport records added: {n_new} | loose matches: "
      f"{len([r for r in report if r.startswith('LOOSE')])}")
print(f"no-geocode failures: {len([r for r in report if r.startswith('NOGEO')])}")
for line in report[:40]:
    print(" ", line)
