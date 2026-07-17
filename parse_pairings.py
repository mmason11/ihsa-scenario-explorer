"""
Parses an IHSA sectional-pairings bracket page (saved HTML) into a list of
(sectional_name, [schools]) — the same shape new_sports.py's ASSIGNMENTS
entries use. Used to transcribe real sectional data; not part of the main
build pipeline (prepare_data.py -> build_v2.py -> build_site.py), just a
one-off tool re-run whenever a new season's pairings post.

Usage:
  1. Fetch a page's raw HTML (real browser headers needed; WebFetch's small-
     model summarization drops team rosters in favor of a results narrative,
     which is useless here — always fetch raw HTML instead):
       curl -s -A "Mozilla/5.0" "https://www.ihsa.org/data/{sport}/{class}pair.htm?r=0" -o out.html
     Sport codes match the tool's own (sob, sog, vbg, bkb, bkg, ba, sbg for
     the multi-class sports; ffg, lcb, lcg, vbb, wpb, wpg for single-class).
     Classes are numbered 1..N (1pair.htm, 2pair.htm, ...).
  2. Preview one file: `python parse_pairings.py out.html`
  3. Or import parse(path) and feed the result into new_sports.py's
     ASSIGNMENTS (flat list for single-class sports, {class: list} dict for
     multi-class — see that file's docstring).

Every team appearing anywhere in a sectional's bracket (winner or not) is
counted as a member of it — the page is a full results tree, not a "who's
paired with whom" listing, so membership has to be inferred from match
lines rather than read off directly.
"""
import re, sys, html

# Two result-line formats seen across sports:
#  numeric: "Match/Game N: TeamA <score>, TeamB <score>[ (note)]"  (soccer/basketball/baseball/softball)
#  volleyball: "Match N: TeamA d. TeamB, <set scores>"
NUMERIC_RE = re.compile(r"(?:Match|Game)\s+\d+:\s*(.+?)\s+\d+(?:\.\d+)?\s*,\s*(.+?)\s+\d+(?:\.\d+)?(?:\s*\(|<)")
DOTWIN_RE = re.compile(r"(?:Match|Game)\s+\d+:\s*(.+?)\s+d\.\s+(.+?),")


def _extract(body, regex):
    teams, seen = [], set()
    for mm in regex.finditer(body):
        for raw in (mm.group(1), mm.group(2)):
            t = html.unescape(re.sub(r"\s+", " ", raw).strip())
            if t not in seen:
                seen.add(t)
                teams.append(t)
    return teams


def parse(path):
    with open(path, encoding="ISO-8859-1") as f:
        content = f.read()

    # auto-detect format once per file: whichever regex fires more on the whole doc
    fmt = NUMERIC_RE if len(NUMERIC_RE.findall(content)) >= len(DOTWIN_RE.findall(content)) else DOTWIN_RE

    # Sectional (<H3>) content runs until the next <H2> or <H3> — a <H2> super-
    # sectional block can sit between two sectionals, and naively splitting on
    # <H3> alone would swallow it into the preceding sectional's roster.
    headers = list(re.finditer(r"<(H2|H3)>\s*(.*?)\s*</\1>", content, flags=re.S))
    sectionals = []
    for i, m in enumerate(headers):
        if m.group(1) != "H3":
            continue
        name = html.unescape(re.sub(r"\s+", " ", m.group(2)).strip())
        start = m.end()
        end = headers[i + 1].start() if i + 1 < len(headers) else len(content)
        body = content[start:end]
        teams = _extract(body, fmt)
        full_name = name if name.endswith("Sectional") else name + " Sectional"
        sectionals.append((full_name, teams))
    return sectionals


if __name__ == "__main__":
    path = sys.argv[1]
    result = parse(path)
    total = 0
    for name, teams in result:
        print(f"{name}  ({len(teams)} teams)")
        for t in teams:
            print("   ", t)
        total += len(teams)
    print(f"\n{len(result)} sectionals, {total} team-slots total")
