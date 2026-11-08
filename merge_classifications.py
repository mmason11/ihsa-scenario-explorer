"""
Merges the per-season extracts in class_pull/*.json into classifications_flags.json
(all 7 enrollment-classed sports) and enrollments.json (current-cycle base figures).

The old pull_classifications.py workflow is dead: ihsa.org replaced the static
color-coded .htm classification pages with a React app at
ihsa.org/schools/enrollments-classifications (Fall / Winter / Spring tabs — a
Spring page exists now, so BA/SBG/SOG finally have official flags). The table is
rendered client-side, so the refresh procedure is browser extraction, not curl:

  1. Open the page in a real browser and run, per season tab, a DOM extractor that
     records each row as [school, enrollment_text, {sport: "2A"+flagchar}] where
     flagchar encodes the cell's background color per the page's Key:
       #FFFF99 yellow  -> c (coop)     #BCEFB4 lt green -> w (waived)
       #FF99CC pink    -> m (multiplier) #000066 dk blue -> s (success)
       #006600 dk green-> p (playup)
  2. Save the chunks as class_pull/{fall,winter,spring}_{a,b}.json
     ({"hdr":[...], "n": rowcount, "unknown":[], "rows":[...]}).
  3. Run this script.

Re-run each cycle (pages post in spring for the following school year).
"""
import json, re

KEEP = {"SOB","VBG","BKB","BKG","BA","SBG","SOG"}
FLAG = {"c":"coop","w":"waived","m":"multiplier","s":"success","p":"playup"}

flags, enroll = {}, {}
for part in ["fall_a","fall_b","winter_a","winter_b","spring_a","spring_b"]:
    d = json.load(open(f"class_pull/{part}.json"))
    assert not d.get("unknown"), (part, d["unknown"])
    for name, en_txt, sports in d["rows"]:
        m = re.match(r"^([\d,]+\.?\d*)", en_txt.strip())
        if m:
            enroll[name] = float(m.group(1).replace(",",""))
        for sp, v in sports.items():
            if sp not in KEEP:
                continue
            mm = re.match(r"^(\d+A)([cwmsp]?)$", v)
            assert mm, (name, sp, v)
            flags.setdefault(name, {})[sp] = {"class": mm.group(1), "flag": FLAG.get(mm.group(2)) or None}

with open("classifications_flags.json","w",encoding="utf-8") as f:
    json.dump(flags, f, indent=1, ensure_ascii=False, sort_keys=True)
with open("enrollments.json","w",encoding="utf-8") as f:
    json.dump(enroll, f, indent=1, ensure_ascii=False, sort_keys=True)
print(f"schools with flags: {len(flags)} | enrollments: {len(enroll)}")
