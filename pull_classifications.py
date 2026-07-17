"""
Parses IHSA's official color-coded School Classifications pages into
classifications_flags.json: {school: {sport: {"class": "2A", "flag": "coop"|"waived"|
"multiplier"|"success"|"playup"|null}}}.

Not part of the main pipeline; a standalone tool re-run each cycle (fetch commands
below) — same spirit as parse_pairings.py / pull_state_finalists.py.

This is the authoritative source for classification-affecting flags that were
previously only guessable:
  - coop: classification is based on a hosted co-op's COMBINED enrollment, not this
    school's own figure — explains the largest share of "actual class higher than
    this tool's own enrollment model predicts" cases (co-op combined enrollment isn't
    modeled anywhere else in this pipeline).
  - waived / multiplier: whether the 1.65x private-school multiplier has an approved
    waiver for this specific program, replacing the "assume every private program is
    multiplied unless the user says otherwise" default with a real per-program answer.
  - success: IHSA's own "success formula" flag — the ground truth for the success
    factor, more reliable than reconstructing it from state-tournament history (see
    pull_state_finalists.py), though it's a same-year snapshot and can't tell you
    what next year's window will look like the way the history-based projection can.
  - playup: the program voluntarily chose to compete in a higher class than its
    enrollment would otherwise place it — a category this tool didn't previously
    account for at all.

Usage:
  1. Fetch each season's page (current cycle folder name changes; check
     ihsa.org/Schools/Enrollments-Classifications for the live one):
       curl -s -A "Mozilla/5.0" "https://www.ihsa.org/data/school/{cycle}/school-classifications-{season}.htm" -o {season}.html
     Once a season has concluded, its page moves to the archive host instead:
       curl -s -A "Mozilla/5.0" "https://archive.ihsa.org/data/school/{cycle}/school-classifications-{season}.htm" -o {season}.html
     Seasons: fall (CCB/CCG/GOB/GOG/SOB/TNG/VBG), winter (BKB/BKG/CHC/DAC/SCB/WR).
     No spring page was found posted or archived under any URL pattern tried for the
     2025-26 cycle as of this writing — BA/SBG/SOG aren't covered by this data yet;
     this tool still uses inferred defaults for those three.
  2. Run this script pointed at the fetched files (edit FILES below, or call
     parse_file()/build() directly) to regenerate classifications_flags.json.
"""
import glob, html, json, re

FILES = ["class_fall.html", "class_winter.html"]  # adjust to your fetched filenames

FLAG_MAP = {
    "bgltyellow": "coop",
    "bgltgreen": "waived",
    "bgpink": "multiplier",
    "bgblue": "success",
    "bggreen": "playup",
}


def parse_file(path):
    with open(path, encoding="ISO-8859-1") as f:
        content = f.read()
    header_m = re.search(r"<TR>\s*<TD[^>]*>School</TD>.*?</TR>", content, re.S)
    sports = re.findall(r'COLSPAN="2">([A-Z]+)</TD>', header_m.group(0))

    rows = {}
    for row_m in re.finditer(r"<TR[^>]*>(.*?)</TR>", content, re.S):
        row = row_m.group(1)
        if "School</TD>" in row:
            continue
        cells = re.findall(r"<TD([^>]*)>(.*?)</TD>", row, re.S)
        if not cells:
            continue
        school = html.unescape(re.sub(r"<[^>]+>", "", cells[0][1])).strip()
        if not school:
            continue
        entry = {}
        for sp, (attrs, val) in zip(sports, cells[2:]):
            text = html.unescape(re.sub(r"<[^>]+>", "", val)).strip().replace("&nbsp;", "").strip()
            if not text:
                continue
            flag = next((name for css, name in FLAG_MAP.items() if css in attrs), None)
            entry[sp] = {"class": text, "flag": flag}
        if entry:
            rows[school] = entry
    return rows


def build(files=FILES):
    out = {}
    for path in files:
        for school, sports in parse_file(path).items():
            out.setdefault(school, {}).update(sports)
    return out


if __name__ == "__main__":
    result = build()
    with open("classifications_flags.json", "w", encoding="utf-8", newline="\n") as f:
        json.dump(result, f, indent=1, ensure_ascii=False, sort_keys=True)
    counts = {}
    for sports in result.values():
        for d in sports.values():
            if d["flag"]:
                counts[d["flag"]] = counts.get(d["flag"], 0) + 1
    print(f"schools: {len(result)}, flag counts: {counts}")
