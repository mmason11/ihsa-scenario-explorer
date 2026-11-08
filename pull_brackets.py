"""
Builds real_brackets.json: {sport: {class: {sectional_name: {"rounds": [
  {"name": str, "matchups": [{"seedA","teamA","scoreA","seedB","teamB","scoreB",
  "winner":"A"|"B"|None}]}
]}}}} — the ACTUAL 2025-26 season seeded brackets (real seeds, real results, every
round) for every sectional in every class the tool tracks, both the 7 sports it
classifies by enrollment and the 6 single-class sports.

Not part of the main build pipeline (prepare_data.py -> build_v2.py ->
build_site.py) — a standalone tool re-run once a season as pairings finalize,
same spirit as new_sports.py/parse_pairings.py/pull_state_finalists.py.

Source: ihsa.org/data/{code}/{class}bracket.htm — a different page family than the
{class}pair.htm results pages those scripts already scrape, but same host/
namespace and sport codes. Unlike pair.htm's plain "Match N: A s, B s" result
lines (membership only, no seeds), bracket.htm renders the actual bracket tree as
an HTML table: one <H2>Sectional Name</H2> per sectional, followed by a
<table class="bracket2011"> whose first row (class="roundwrap") names each
round's column-group left to right, and whose data rows carry
`<td class="team">(N) Name</td>` immediately followed by
`<td class="score">S</td>`, with the winner's cells wrapped in <B>. Column
position — honoring rowspan carry-over from earlier rows, since a naive per-row
<td> scan drifts one column short whenever it follows an active
rowspan="4"/"8"/"16" brace cell — determines which round-group a team-cell
belongs to. Every round-column turns out to be an independently complete,
self-contained list of that round's real entrants in top-to-bottom document
order: a team that got a bye (or won an earlier preliminary trim-in game,
labeled "REGIONAL QUARTERFINALS" here even for sectionals where only one pair of
schools needed it) simply has no entry in the round before the one they're
first listed in, so no special bye-detection logic is needed — consecutive
entries within a round pair up correctly on their own. Verified against the
Washington Sectional (SOB, 2A) this was built to fix: Washington, seed 2, beat
Pekin 9-0 then Morton 1-0 in the regional final; Morton, seed 3, beat
Bloomington (H.S.) 1-0 in the first round — exactly matching ihsa.org's own
seeded-bracket page, and directly contradicting the tool's old synthetic
MaxPreps reseed, which had fabricated Morton as an unseeded 16-seed with a bye.

Usage:
  1. Fetch each (sport, class) page's raw HTML:
       curl -s -A "Mozilla/5.0" "https://www.ihsa.org/data/{code}/{class}bracket.htm?r=0" -o out.html
     Sport codes: sob, sog, vbg, bkb, bkg, ba, sbg (multi-class, class numbered
     1..3 or 1..4 per SPORT_CLASSES below); ffg, lcb, lcg, vbb, wpb, wpg
     (single-class, always class "1"). Save into FETCH_DIR named
     {SPORT}_{class}.html (e.g. SOB_2.html, VBB_1.html) — sport/class are read
     back out of the filename (unlike pull_state_finalists.py, which reads the
     season year from the page itself, this page doesn't print its class
     anywhere reliable to parse back out).
  2. Run this script (or import build()) to regenerate real_brackets.json.
"""
import glob, html, json, os, re

FETCH_DIR = "bracket_pages"

SINGLE_CLASS_SPORTS = {"FLGG", "LAXB", "LAXG", "VBB", "WPB", "WPG"}
SPORT_CODES = {
    "SOB": "sob", "SOG": "sog", "VBG": "vbg", "BKB": "bkb", "BKG": "bkg",
    "BA": "ba", "SBG": "sbg",
    "FLGG": "ffg", "LAXB": "lcb", "LAXG": "lcg", "VBB": "vbb", "WPB": "wpb", "WPG": "wpg",
}
SPORT_CLASSES = {
    "SOB": ["1", "2", "3"], "SOG": ["1", "2", "3"],
    "VBG": ["1", "2", "3", "4"], "BKB": ["1", "2", "3", "4"],
    "BKG": ["1", "2", "3", "4"], "BA": ["1", "2", "3", "4"], "SBG": ["1", "2", "3", "4"],
}
CLASS_LABELS = {"1": "1A", "2": "2A", "3": "3A", "4": "4A"}

TEAM_RE = re.compile(r"^\s*(?:<B>)?\s*\((\d+)\)\s*(.+?)\s*(?:</B>)?\s*$", re.S)


def _cells(tr, occupied):
    """[(col, attrs, text)] for the <td>s in one row, skipping columns still
    occupied by a still-active rowspan from an earlier row, and updating
    `occupied` (col -> rows remaining, this row included) for the next row."""
    out = []
    col = 0
    for attrs, text in re.findall(r"<td([^>]*)>(.*?)</td>", tr, flags=re.S):
        while occupied.get(col, 0) > 0:
            col += 1
        cs = re.search(r'colspan="(\d+)"', attrs)
        span = int(cs.group(1)) if cs else 1
        rs = re.search(r'rowspan="(\d+)"', attrs)
        rowspan = int(rs.group(1)) if rs else 1
        out.append((col, attrs, text))
        for k in range(span):
            occupied[col + k] = max(occupied.get(col + k, 0), rowspan)
        col += span
    return out


def _tick(occupied):
    for c in list(occupied):
        occupied[c] -= 1
        if occupied[c] <= 0:
            del occupied[c]


def _parse_team(text):
    winner = "<B>" in text
    m = TEAM_RE.match(text)
    if not m:
        return None
    seed, name = m.groups()
    return {"seed": int(seed), "name": html.unescape(re.sub(r"\s+", " ", name)).strip(),
            "winner": winner}


def parse_sectional(content):
    """One sectional's H2-delimited content -> [{"name","matchups":[...]}]."""
    m = re.search(r'<table[^>]*class="bracket2011"[^>]*>(.*?)</table>', content, flags=re.S)
    if not m:
        return []
    trs = re.findall(r"<tr[^>]*>(.*?)</tr>", m.group(1), flags=re.S)
    if not trs:
        return []

    occ = {}
    header_cells = _cells(trs[0], occ)
    _tick(occ)

    round_names, col_round = [], {}
    for col, attrs, text in header_cells:
        if 'class="level"' in attrs:
            cs = re.search(r'colspan="(\d+)"', attrs)
            span = int(cs.group(1)) if cs else 1
            r = len(round_names)
            round_names.append(html.unescape(re.sub(r"\s+", " ", text)).strip())
            for k in range(span):
                col_round[col + k] = r

    by_round = {}
    for tr in trs[1:]:
        row_cells = _cells(tr, occ)
        # Plain <td class="score">N</td> immediately in the same row as its team
        # cell (soccer/basketball/baseball/softball) is reliable to capture. Girls
        # volleyball instead prints a <td class="longscore">25-2, 25-9</td> set
        # score attached to the WINNER's entry in the round AFTER the one the
        # match was actually played in (i.e. row-adjacency doesn't mean
        # same-match here) — capturing it would misattribute a round's score to
        # a different round's matchup, so it's deliberately left as None rather
        # than shown wrong. Boys volleyball prints no score at all either way.
        row_score = None
        for _, attrs, text in row_cells:
            if 'class="score"' in attrs:
                sm = re.search(r"\d+", text)
                row_score = int(sm.group(0)) if sm else None
                break
        for col, attrs, text in row_cells:
            if 'class="team"' not in attrs:
                continue
            team = _parse_team(text)
            if team is None:
                continue
            team["score"] = row_score
            r = col_round.get(col)
            if r is not None:
                by_round.setdefault(r, []).append(team)
        _tick(occ)

    rounds = []
    for r in sorted(by_round):
        entries = by_round[r]
        matchups = []
        for i in range(0, len(entries) - 1, 2):
            a, b = entries[i], entries[i + 1]
            winner = "A" if a["winner"] else ("B" if b["winner"] else None)
            matchups.append({
                "seedA": a["seed"], "teamA": a["name"], "scoreA": a["score"],
                "seedB": b["seed"], "teamB": b["name"], "scoreB": b["score"],
                "winner": winner,
            })
        if matchups:
            name = round_names[r] if r < len(round_names) else f"Round {r}"
            rounds.append({"name": name, "matchups": matchups})
    return rounds


def parse_class_page(path):
    """One {sport}/{class}bracket.htm -> [(sectional_name, {"rounds": [...]})],
    preserving every block even if two share the same raw H2 text (seen for
    LAXG, whose bracket page uses a bare " Sectional" heading with no location
    — resolved by roster-overlap in _dedupe_names below, not lost here)."""
    with open(path, encoding="ISO-8859-1") as f:
        content = f.read()
    headers = list(re.finditer(r"<H2>\s*(.*?)\s*</H2>", content, flags=re.S))
    out = []
    for i, m in enumerate(headers):
        name = html.unescape(re.sub(r"\s+", " ", m.group(1)).strip())
        if name == "Super Sixteen":
            continue
        start = m.end()
        end = headers[i + 1].start() if i + 1 < len(headers) else len(content)
        rounds = parse_sectional(content[start:end])
        if rounds:
            out.append((name, {"rounds": rounds}))
    return out


def _norm(s):
    import unicodedata
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = s.lower().replace("[coop]", "")
    s = re.sub(r"\[.*?\]", "", s)
    s = re.sub(r"[^a-z0-9()]+", "", s)
    return s


def _block_teams(block):
    teams = set()
    for rnd in block["rounds"]:
        for mu in rnd["matchups"]:
            teams.add(mu["teamA"])
            teams.add(mu["teamB"])
    return teams


def _dedupe_names(sport, blocks):
    """blocks: [(raw_name, block)]. When names collide (every sectional shares
    the same generic heading), re-derive each block's real name by matching its
    team roster against new_sports.py's ASSIGNMENTS for this sport — that data
    was transcribed from a different IHSA page family that does print real
    sectional names. Falls through to the raw name untouched when there's no
    collision (the normal case for every sport but LAXG so far)."""
    names = [n for n, _ in blocks]
    if len(set(names)) == len(names):
        return dict(blocks)
    from new_sports import ASSIGNMENTS
    secs = ASSIGNMENTS.get(sport)
    if not isinstance(secs, list):
        print(f"WARN {sport}: duplicate sectional names but no flat ASSIGNMENTS to resolve against")
        return {f"{n} {i}": b for i, (n, b) in enumerate(blocks)}
    known = [(sec_name, {_norm(s) for s in schools}) for sec_name, schools in secs]
    out = {}
    for raw_name, block in blocks:
        block_teams = {_norm(t) for t in _block_teams(block)}
        best_name, best_overlap = raw_name, -1
        for sec_name, sec_teams in known:
            overlap = len(block_teams & sec_teams)
            if overlap > best_overlap:
                best_name, best_overlap = sec_name, overlap
        if best_name in out:
            print(f"WARN {sport}: '{best_name}' matched twice, keeping first")
            continue
        out[best_name] = block
    return out


def build(fetch_dir=FETCH_DIR):
    out = {}
    for path in sorted(glob.glob(os.path.join(fetch_dir, "*.html"))):
        base = os.path.splitext(os.path.basename(path))[0]
        m = re.match(r"([A-Z]+)_(\d+)$", base)
        if not m:
            print(f"WARN unrecognized filename, skipping: {path}")
            continue
        sport, class_num = m.groups()
        class_label = "S" if sport in SINGLE_CLASS_SPORTS else CLASS_LABELS.get(class_num, class_num)
        blocks = parse_class_page(path)
        sectionals = _dedupe_names(sport, blocks)
        out.setdefault(sport, {})[class_label] = sectionals
    return out


if __name__ == "__main__":
    result = build()
    with open("real_brackets.json", "w", encoding="utf-8", newline="\n") as f:
        json.dump(result, f, indent=1, ensure_ascii=False, sort_keys=True)
    for sport in sorted(result):
        for cls, secs in sorted(result[sport].items()):
            print(sport, cls, len(secs), "sectionals")
