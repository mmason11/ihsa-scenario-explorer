"""
Builds state_finalists.json: {sport: {year: [schools that reached the state final 4]}}
for the 7 multi-class sports this tool classifies by enrollment, across the seasons
needed for the rolling-three-year success-factor window (see template.html's
CLASS_CUTOFFS comment for the exact rule).

Not part of the main build pipeline (prepare_data.py -> build_v2.py -> build_site.py) —
a standalone tool re-run once a year as the window rolls forward, same spirit as
parse_pairings.py.

Usage:
  1. Fetch each (sport, year, class) bracket page's raw HTML. Two URL families:
     - Current season (whatever's "live" on ihsa.org right now):
         curl -s -A "Mozilla/5.0" "https://www.ihsa.org/data/{sport}/{class}pair.htm?r=0" -o out.html
     - Prior seasons, via the dated archive (goes back at least to 2021-22):
         curl -s -A "Mozilla/5.0" "https://www.ihsa.org/archive/{sport}/{year}/{class}pair.htm" -o out.html
     Sport codes: sob, sog (3 classes), vbg, bkb, bkg, ba, sbg (4 classes). Year format
     "2022-23". Filename just needs to start with the sport code — the season year is
     read from the page's own H1, not the filename — so any naming works, e.g.
     history/{sport}_{year}_{class}.html or the current season's {sport}{class}.html.
  2. Run this script pointed at the directory holding those files (edit FETCH_DIR below,
     or call state_final_teams()/build() directly) to regenerate state_finalists.json.

Every bracket page's first <H2> section is always "State Final Tournament" — the 4
teams that reached state finals weekend (2 super-sectional winners' semifinal, 3rd
place, and championship). IHSA awards trophies to all 4, matching this tool's (and the
user's) definition of "state trophy" = reaching the final four, regardless of finish.
Reuses parse_pairings.py's format auto-detection (numeric "Match/Game N: A s, B s" vs.
volleyball's "Match N: A d. B, set-scores") since these are the same page family.

Name matching: printed names are canonicalized against schools_data.json the same way
build_v2.py does (normalize + strip parens + coop-tag stripping), with a couple of
manual fixes for names printed without their usual city prefix. Unmatched names (e.g.
a school not otherwise in the roster) are dropped with a warning rather than guessed.
"""
import glob, json, os, re, unicodedata
from parse_pairings import NUMERIC_RE, DOTWIN_RE, _extract

FETCH_DIR = "state_final_pages"  # directory of raw HTML files, see docstring for naming

MANUAL_NAME_FIXES = {
    "West Central [Coop]": "Biggsville (West Central)",
}


def state_final_teams(path):
    """Returns (season_year, [4 finalist teams]) — season_year comes from the page's own
    H1 ("...Schedule & Scores &#151; 2025-26"), not the filename, so it's correct
    regardless of what the file happened to be named when fetched."""
    with open(path, encoding="ISO-8859-1") as f:
        content = f.read()
    ym = re.search(r"&#151;\s*(\d{4}-\d{2})", content)
    year = ym.group(1) if ym else None
    fmt = NUMERIC_RE if len(NUMERIC_RE.findall(content)) >= len(DOTWIN_RE.findall(content)) else DOTWIN_RE
    headers = list(re.finditer(r"<(H2|H3)>\s*(.*?)\s*</\1>", content, flags=re.S))
    for i, m in enumerate(headers):
        name = re.sub(r"\s+", " ", m.group(2)).strip()
        if name != "State Final Tournament":
            continue
        start = m.end()
        end = headers[i + 1].start() if i + 1 < len(headers) else len(content)
        return year, _extract(content[start:end], fmt)
    return year, []


def _norm(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = s.lower().replace("[coop]", "")
    s = re.sub(r"\[.*?\]", "", s)
    s = re.sub(r"\b([a-z])\.\-", "", s)
    s = re.sub(r"\b([a-z])\. ", "", s)
    s = re.sub(r"[^a-z0-9()]+", "", s)
    return s


def build(fetch_dir=FETCH_DIR, master_json="schools_data.json"):
    with open(master_json, encoding="utf-8") as f:
        data = json.load(f)
    master_by_norm = {_norm(s["n"]): s["n"] for s in data["schools"]}

    def canon(printed):
        if printed in MANUAL_NAME_FIXES:
            return MANUAL_NAME_FIXES[printed]
        n = _norm(printed)
        if n in master_by_norm:
            return master_by_norm[n]
        base = re.sub(r"\s*\(.*?\)\s*", "", printed).strip()
        nb = _norm(base)
        if nb in master_by_norm:
            return master_by_norm[nb]
        print(f"WARN unmatched finalist name (dropped): {printed!r}")
        return None

    raw = {}  # sport -> year -> set(printed names)
    for path in sorted(glob.glob(os.path.join(fetch_dir, "*.html"))):
        base = os.path.splitext(os.path.basename(path))[0]
        # sport is the leading letters of the filename regardless of naming convention
        # used to fetch it ({sport}_{year}_{class}.html or {sport}{class}.html); the
        # season year comes from the page content itself, not the filename.
        sport = re.match(r"[a-z]+", base).group(0)
        year, teams = state_final_teams(path)
        if year is None:
            print(f"WARN couldn't find a season year in {path}, skipping")
            continue
        raw.setdefault(sport.upper(), {}).setdefault(year, set()).update(teams)

    out = {}
    for sport, years in raw.items():
        out[sport] = {}
        for year, teams in years.items():
            canonical = sorted({c for t in teams if (c := canon(t))})
            out[sport][year] = canonical
    return out


if __name__ == "__main__":
    result = build()
    with open("state_finalists.json", "w", encoding="utf-8", newline="\n") as f:
        json.dump(result, f, indent=1, ensure_ascii=False, sort_keys=True)
    for sport in sorted(result):
        print(sport, {yr: len(v) for yr, v in result[sport].items()})
