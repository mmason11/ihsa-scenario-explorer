"""
Parses MaxPreps team-strength rankings into maxpreps_ratings.json:
{sport: {class: {school: {"rank":, "record":, "rating":, "str":}}}}, for the 7
enrollment-classed sports this tool tracks via CLASS_CUTOFFS in template.html
(BA/BKB/BKG/SBG/VBG, classes 1A-4A; SOB/SOG, classes 1A-3A) plus the 3 single-class
sports VBB/LAXB/LAXG (class key "S", matching how school.c[sport] already uses "S").
Water polo (WPB/WPG) and girls flag football (FLGG) are excluded — no usable MaxPreps
rankings found for either: water polo's MaxPreps landing page has no inline rankings
table, and flag football's URL slug couldn't be found.

Not part of the main build pipeline (prepare_data.py -> build_v2.py -> build_site.py)
— a standalone tool re-run each season, same spirit as pull_state_finalists.py /
pull_classifications.py. Unlike those, this one fetches its own pages (stdlib urllib,
no new dependency) rather than asking you to run curl by hand: MaxPreps' rankings
pages are Next.js server-rendered, so a plain GET returns the exact data the page's
React component consumes, embedded in a <script id="__NEXT_DATA__"> JSON blob — far
more reliable to parse than scraping rendered table markup. Every fetched page is
still saved to maxpreps_pages/ for auditability, matching the "raw pages saved
locally" ethos of the other pull scripts even though the fetch itself is automated.

Per-sport class GUIDs (MaxPreps' "statedivisionid") are discovered from a single seed
page rather than needing one URL per class: a classed sport's rankings page embeds
its OTHER classes' {label, GUID} pairs too (props.pageProps.initRankingsStoreData.
contextOptions), so fetching just one class's URL reveals the rest.

Usage:
  1. Fill in SEED_URLS below with one Rankings-page URL per sport (any single class
     for the classed sports) — visit MaxPreps, navigate to Illinois -> that
     sport/gender's Rankings page, copy the URL. SOB's is already filled in (from the
     2A boys soccer rankings page). Boy/girl and season are NOT disambiguated by the
     URL's sport slug alone (e.g. "soccer" covers both boys-Fall and girls-Spring) —
     that's exactly why a real seed URL per sport is needed rather than guessing.
  2. Run: python pull_maxpreps_rankings.py
     Pass --refresh to re-fetch pages already saved (e.g. mid-season rating updates).
     Sports left as None in SEED_URLS are skipped with a note, not an error.
"""
import glob, json, os, re, sys, time
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit
from urllib.request import Request, urlopen

from pull_state_finalists import _norm

FETCH_DIR = "maxpreps_pages"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")
REQUEST_DELAY = 0.3  # seconds between fetches, polite/conservative

# One rankings-page URL per sport (any single class for the classed sports — see
# docstring). Fill these in from MaxPreps: Illinois -> sport/gender -> Rankings.
SEED_URLS = {
    "SOB": "https://www.maxpreps.com/il/soccer/25-26/class/2a/rankings/1/?statedivisionid=fd3a9a2b-6961-4398-8883-6d3a9c2bddab",
    "SOG": "https://www.maxpreps.com/il/soccer/girls/spring/25-26/class/2a/rankings/1/?statedivisionid=3302b6c5-efed-4caf-9f6f-759dbcdd9800",
    "VBG": "https://www.maxpreps.com/il/volleyball/25-26/class/class-3a/rankings/1/?statedivisionid=e1b47a91-48a8-4aeb-b289-8f18e5225a17",
    "VBB": "https://www.maxpreps.com/il/volleyball/boys/25-26/rankings/1/",
    "BKB": "https://www.maxpreps.com/il/basketball/25-26/class/class-3a/rankings/1/?statedivisionid=26c5d620-fd99-47d5-8644-ef9cc38e6eb1",
    "BKG": "https://www.maxpreps.com/il/basketball/girls/25-26/class/class-3a/rankings/1/?statedivisionid=1e0d4f88-1317-4a02-b0ad-397e566e9b4a",
    "BA": "https://www.maxpreps.com/il/baseball/25-26/class/class-3a/rankings/1/?statedivisionid=c126f0e1-4480-400c-bc21-69da283c5297",
    "SBG": "https://www.maxpreps.com/il/softball/25-26/class/class-3a/rankings/1/?statedivisionid=2af4acc1-b681-4151-8bf1-7aa8420bbaee",
    "LAXB": "https://www.maxpreps.com/il/lacrosse/25-26/rankings/1/?schoolid=b50965a7-57a2-48ff-9bed-65c735ea9738",
    "LAXG": "https://www.maxpreps.com/il/lacrosse/girls/25-26/rankings/1/?schoolid=9d8b368e-4ab9-4e18-a99f-90077f8df5ea",
}

MANUAL_NAME_FIXES = {
    # "MaxPreps schoolName": "Canonical schools_data.json name" — names MaxPreps
    # abbreviates, reorders, or informally shortens differently than this repo's
    # "City (School)" convention does, verified by hand against schools_data.json.
    "Marmion": "Aurora (Marmion Academy)",
    "Homewood-Flossmoor": "Flossmoor (Homewood-F.)",
    "Bloom": "Chicago Heights (Bloom Twp.)",
    "Solorio": "Chicago (Solorio Academy)",
    "Oak Park-River Forest": "Oak Park (O.P.-River Forest)",
    "Normal West": "Normal (Community West)",
    "Elk Grove": "Elk Grove Village (E.G.)",
    "East Alton-Wood River": "Wood River (East Alton-W.R.)",
    "Mt. Carmel": "Chicago (Mt. Carmel)",
    "Washington": "Washington",
    "Lane Tech": "Chicago (Lane)",
    "Marian Catholic": "Chicago Heights (Marian)",
    "Marian Central Catholic": "Woodstock (Marian)",
    "Montini Catholic": "Lombard (Montini)",
    "Bishop McNamara": "Kankakee (McNamara)",
    "Joliet Catholic": "Joliet (Catholic Academy)",
    "Father McGivney Catholic": "Glen Carbon (Father McGivney)",
    "IC Catholic Prep": "Elmhurst (IC Catholic)",
}


def _fetch(url):
    req = Request(url, headers={"User-Agent": UA, "Accept": "text/html"})
    with urlopen(req, timeout=20) as resp:
        return resp.read().decode("utf-8", errors="replace")


def _next_data(html_text):
    m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html_text, re.S)
    return json.loads(m.group(1)) if m else None


def _page_path(sport, class_label, page):
    return os.path.join(FETCH_DIR, f"{sport}_{class_label}_{page}.html")


def _save(path, html_text):
    os.makedirs(FETCH_DIR, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html_text)


def page_url(seed_url, url_slug, gid, page):
    """Builds another page's URL by substituting into the CONFIRMED-WORKING seed
    URL's own structure (class segment, page number, statedivisionid) rather than
    reconstructing sport-slug/season from scratch — robust to per-sport URL shape
    differences we haven't individually verified.

    Always drops any "schoolid" query param: MaxPreps' own share links carry it (it
    highlights/centers that school in the list), but its PRESENCE makes the site
    ignore the /rankings/{page}/ path segment entirely and always serve page 1 —
    confirmed by comparing a schoolid-bearing URL's page 2 (returned rank 1-25 again)
    against the same URL with schoolid stripped (correctly returned rank 26-50).
    Dropped via proper query-string parsing rather than a one-off string edit on
    whichever seed URLs happened to have it, so this can't quietly regress again."""
    url = seed_url
    if "/class/" in url:
        url = re.sub(r"(/class/)[^/]+(/)", lambda m: m.group(1) + url_slug + m.group(2), url)
    url = re.sub(r"(/rankings/)\d+(/)", lambda m: m.group(1) + str(page) + m.group(2), url)
    parts = urlsplit(url)
    q = dict(parse_qsl(parts.query))
    q.pop("schoolid", None)
    if gid:
        q["statedivisionid"] = gid
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(q), parts.fragment))


def discover(sport, seed_url, refresh):
    """Fetches the seed page once; returns [(class_key, url_slug, gid_or_None,
    total_or_None)] — total_count is known immediately only for the seed's own class,
    others get filled in when their first page is fetched.

    contextOptions labels aren't consistent across sports — soccer/basketball use
    bare "1A"/"2A", volleyball uses "Class 1A" with a "class-1a" URL slug (hyphenated,
    "class-" prefixed) rather than bare "1a". class_key is the clean label for
    storage/output (matching this tool's own "1A"/"2A" class values); url_slug is
    whatever string the URL's /class/.../ segment actually needs, derived the same
    mechanical way MaxPreps itself seems to (lowercase, spaces -> hyphens) — verified
    against both the soccer ("2A" -> "2a") and volleyball ("Class 3A" -> "class-3a")
    shapes actually seen."""
    path = _page_path(sport, "SEEDTMP", 1)
    if not refresh and os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            html_text = f.read()
    else:
        html_text = _fetch(seed_url)
        time.sleep(REQUEST_DELAY)
    data = _next_data(html_text)
    if data is None:
        raise RuntimeError("couldn't find __NEXT_DATA__ in seed page")
    pp = data["props"]["pageProps"]
    rld = pp["rankingsListData"]
    opts = pp.get("initRankingsStoreData", {}).get("contextOptions", [])
    classes = [(o["label"], o["value"]) for o in opts if o.get("value") and o["value"] != "unselected"]

    seed_gid_m = re.search(r"statedivisionid=([\w-]+)", seed_url)
    seed_gid = seed_gid_m.group(1) if seed_gid_m else None

    if os.path.exists(path):
        os.remove(path)

    if not classes:
        # single-class sport — the seed page IS the whole (only) field
        _save(_page_path(sport, "S", 1), html_text)
        return [("S", "S", None, rld["totalCount"])]

    result = []
    for label, gid in classes:
        class_key = re.sub(r"^class\s+", "", label, flags=re.I).strip()
        url_slug = label.lower().replace(" ", "-")
        if gid == seed_gid:
            _save(_page_path(sport, class_key, 1), html_text)
            result.append((class_key, url_slug, gid, rld["totalCount"]))
        else:
            result.append((class_key, url_slug, gid, None))
    return result


def fetch_all_pages(sport, seed_url, classes, refresh):
    """Fetches every page for every (class_key, url_slug, gid) in classes, saving raw
    HTML under FETCH_DIR. Page 1 of a class not already cached (via discover()) is
    fetched to learn its total_count, then remaining pages are fetched to cover it."""
    for class_key, url_slug, gid, total in classes:
        page = 1
        seen = 0
        while total is None or seen < total:
            path = _page_path(sport, class_key, page)
            if not refresh and os.path.exists(path):
                with open(path, encoding="utf-8") as f:
                    data = _next_data(f.read())
            else:
                url = page_url(seed_url, url_slug, gid, page)
                try:
                    html_text = _fetch(url)
                except (HTTPError, URLError) as e:
                    print(f"ERROR {sport} {class_key} page {page}: {e}")
                    break
                _save(path, html_text)
                time.sleep(REQUEST_DELAY)
                data = _next_data(html_text)
            if data is None:
                print(f"WARN {sport} {class_key} page {page}: no data, stopping this class")
                break
            rld = data["props"]["pageProps"]["rankingsListData"]
            total = total if total is not None else rld["totalCount"]
            seen += len(rld["rankings"])
            if not rld["rankings"]:
                break
            page += 1


def ensure_pages_fetched(refresh=False):
    for sport, seed_url in SEED_URLS.items():
        if not seed_url:
            print(f"SKIP {sport}: no seed URL set in SEED_URLS")
            continue
        try:
            classes = discover(sport, seed_url, refresh)
        except Exception as e:
            print(f"ERROR {sport}: discovery failed ({e})")
            continue
        fetch_all_pages(sport, seed_url, classes, refresh)


def parse_file(path):
    """Returns a list of {"school","city","rank","record","rating","str"} dicts from
    one saved page. City is pulled out of schoolFormattedName when present (it's
    sometimes omitted, e.g. when the school name IS the city) — used only to
    disambiguate same-name schools in different cities during matching."""
    with open(path, encoding="utf-8") as f:
        data = _next_data(f.read())
    if data is None:
        return []
    rld = data["props"]["pageProps"]["rankingsListData"]
    rows = []
    for r in rld["rankings"]:
        formatted = r.get("schoolFormattedName") or ""
        fm = re.search(r"\(([^,)]+),?\s*[A-Z]{2}\)$", formatted)
        if fm:
            city = fm.group(1).strip()
        elif re.search(r"\(\s*[A-Z]{2}\s*\)$", formatted):
            # MaxPreps omits the city entirely when it's identical to the school
            # name (e.g. "Morton (IL)" for the town of Morton's own high school)
            # rather than printing "Morton (Morton, IL)" — infer city == school
            # name in that case rather than leaving it unresolved, since an
            # unresolved city here is exactly what makes an otherwise-unambiguous
            # match (like "Morton") look ambiguous against an unrelated
            # same-named school elsewhere (e.g. "Berwyn-Cicero (Morton)").
            city = r["schoolName"]
        else:
            city = None
        rows.append({"school": r["schoolName"], "city": city, "rank": r["rank"],
                     "record": r["overall"], "rating": r["rating"], "str": r["strength"]})
    return rows


def _flat(s):
    """Normalizes AND strips parens (unlike the shared _norm, which keeps them) —
    MaxPreps names never carry a "(...)" wrapper, so matching keys shouldn't either.
    Also unifies Saint/St. and Mount/Mt., which this dataset spells inconsistently
    and MaxPreps doesn't necessarily abbreviate the way schools_data.json does."""
    s = re.sub(r"\bsaint\b", "st", s, flags=re.I)
    s = re.sub(r"\bmount\b", "mt", s, flags=re.I)
    return _norm(s).replace("(", "").replace(")", "")


def build(fetch_dir=FETCH_DIR, master_json="schools_data.json"):
    with open(master_json, encoding="utf-8") as f:
        data = json.load(f)

    # MaxPreps prints team names in several shapes that don't line up with this
    # repo's "City (School)" convention: sometimes just the bare city (the town's
    # only public school, e.g. "Elgin" for "Elgin (H.S.)"), sometimes city+suffix
    # concatenated with no separator ("St. Charles North" for "St. Charles (North)").
    # So each schools_data.json entry is indexed under every plausible candidate
    # string it might be printed as, not just the school-only portion.
    # Suffixes that just mean "the town's one public school" — MaxPreps prints these
    # as the bare city name. Deliberately NOT including ambiguous ones like
    # "Community" (e.g. Oak Lawn has both "(Community)" and "(Richards)" — bare "Oak
    # Lawn" can't safely resolve to either, so it correctly falls through to a WARN).
    GENERIC_SUFFIXES = {"H.S.", "HS", "SR.", "SR", "TWP.", "TWP"}
    by_key = {}
    for s in data["schools"]:
        n = s["n"]
        m = re.match(r"^(.*?)\s*\((.+)\)$", n)
        if m:
            city, school = m.group(1), m.group(2)
            candidates = {school, f"{city} {school}"}
            if school.upper() in GENERIC_SUFFIXES:
                candidates.add(city)
        else:
            city, candidates = n, {n}
        for cand in candidates:
            by_key.setdefault(_flat(cand), []).append((n, city))

    def canon(printed_school, printed_city):
        if printed_school in MANUAL_NAME_FIXES:
            return MANUAL_NAME_FIXES[printed_school]
        candidates = by_key.get(_flat(printed_school), [])
        if not candidates and printed_city:
            # bare schoolName alone didn't resolve — try it combined with the
            # separately-reported city, in case that's what disambiguates it
            candidates = by_key.get(_flat(f"{printed_city} {printed_school}"), [])
        if not candidates:
            print(f"WARN unmatched maxpreps school (dropped): {printed_school!r}")
            return None
        uniq = sorted(set(candidates))
        if len(uniq) == 1:
            return uniq[0][0]
        if printed_city:
            matches = [n for n, city in uniq if _flat(city) == _flat(printed_city)]
            if len(matches) == 1:
                return matches[0]
        print(f"WARN ambiguous maxpreps school {printed_school!r} "
              f"(candidates: {[n for n, _ in uniq]}), dropped")
        return None

    raw = {}  # sport -> class -> school -> row
    for path in sorted(glob.glob(os.path.join(fetch_dir, "*.html"))):
        base = os.path.splitext(os.path.basename(path))[0]
        sport, class_label, _page = base.split("_")
        for r in parse_file(path):
            name = canon(r["school"], r["city"])
            if not name:
                continue
            raw.setdefault(sport, {}).setdefault(class_label, {})[name] = {
                "rank": r["rank"], "record": r["record"],
                "rating": r["rating"], "str": r["str"]}
    return raw


if __name__ == "__main__":
    ensure_pages_fetched(refresh="--refresh" in sys.argv)
    result = build()
    with open("maxpreps_ratings.json", "w", encoding="utf-8", newline="\n") as f:
        json.dump(result, f, indent=1, ensure_ascii=False, sort_keys=True)
    for sport in sorted(result):
        print(sport, {cls: len(v) for cls, v in result[sport].items()})
