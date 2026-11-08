"""
One-off helper for the Nov 2026 fall refresh: re-parses the 2026-27 fall
pairings (fall_pull/{sob,vbg,ffg}_{N}pair.htm, fetched via the browser relay)
with parse_pairings.parse() and splices the resulting FLGG / SOB / VBG entries
into new_sports.py's ASSIGNMENTS literal in place, leaving every other sport's
text untouched (so diffs stay reviewable). Same spirit as parse_pairings.py:
not part of the main pipeline, kept for the next seasonal refresh.
"""
import re
from parse_pairings import parse

SRC = "new_sports.py"

NEW = {
    "FLGG": parse("fall_pull/ffg_1pair.htm"),  # single-class: flat list
    "SOB": {f"{n}A": parse(f"fall_pull/sob_{n}pair.htm") for n in (1, 2, 3)},
    "VBG": {f"{n}A": parse(f"fall_pull/vbg_{n}pair.htm") for n in (1, 2, 3, 4)},
}


def fmt_school_list(schools, indent):
    """Wrap the quoted school names at ~95 chars, matching the existing style."""
    lines, cur = [], indent
    for s in schools:
        tok = '"%s", ' % s
        if len(cur) + len(tok) > 97 and cur.strip():
            lines.append(cur.rstrip())
            cur = indent
        cur += tok
    if cur.strip():
        lines.append(cur.rstrip())
    return "\n".join(lines)


def fmt_sectionals(secs, pad):
    out = []
    for name, schools in secs:
        out.append('%s("%s", [' % (pad, name.replace('"', '\\"')))
        out.append(fmt_school_list(schools, pad + " "))
        out.append("%s])," % pad)
    return "\n".join(out)


def fmt_entry(sport, data):
    if isinstance(data, dict):
        body = []
        for kl, secs in data.items():
            body.append(' "%s": [' % kl)
            body.append(fmt_sectionals(secs, "  "))
            body.append(" ],")
        return '"%s": {\n%s\n},' % (sport, "\n".join(body))
    return '"%s": [\n%s\n],' % (sport, fmt_sectionals(data, " "))


def find_entry_span(text, sport):
    """Span of `"SPORT": [...],` / `"SPORT": {...},` at ASSIGNMENTS top level."""
    m = re.search(r'^"%s": ([\[{])' % sport, text, flags=re.M)
    if not m:
        raise SystemExit(f"entry {sport} not found")
    opener = m.group(1)
    closer = {"[": "]", "{": "}"}[opener]
    depth = 0
    i = m.start(1)
    in_str = False
    while i < len(text):
        ch = text[i]
        if in_str:
            if ch == "\\":
                i += 2
                continue
            if ch == '"':
                in_str = False
        elif ch == '"':
            in_str = True
        elif ch == opener:
            depth += 1
        elif ch == closer:
            depth -= 1
            if depth == 0:
                end = i + 1
                if text[end:end + 1] == ",":
                    end += 1
                return m.start(), end
        i += 1
    raise SystemExit(f"unbalanced entry {sport}")


def main():
    with open(SRC, encoding="utf-8") as f:
        text = f.read()
    for sport, data in NEW.items():
        start, end = find_entry_span(text, sport)
        text = text[:start] + fmt_entry(sport, data) + text[end:]
        n = (sum(len(t) for _, t in data) if isinstance(data, list)
             else sum(len(t) for secs in data.values() for _, t in secs))
        print(f"{sport}: replaced with 2026-27 data ({n} team-slots)")
    with open(SRC, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    # sanity: file still imports and shapes hold
    import importlib, new_sports
    importlib.reload(new_sports)
    a = new_sports.ASSIGNMENTS
    assert isinstance(a["FLGG"], list) and len(a["FLGG"]) == 8
    assert set(a["SOB"]) == {"1A", "2A", "3A"} and all(len(v) == 8 for v in a["SOB"].values())
    assert set(a["VBG"]) == {"1A", "2A", "3A", "4A"} and all(len(v) == 8 for v in a["VBG"].values())
    print("new_sports.py re-imported OK; shapes verified")


if __name__ == "__main__":
    main()
