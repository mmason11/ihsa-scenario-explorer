"""
Build the deployed page from template.html + schools_data.json.

template.html is the full page (markup, CSS, grouping/travel JS) with a
placeholder in place of the embedded data: `const RAW = __RAW_DATA_JSON__;`

Run this after editing template.html or schools_data.json (e.g. after
resolving a school on the review list, or re-running build_v2.py).
Outputs: index.html
"""
import json

PLACEHOLDER = "__RAW_DATA_JSON__"


def main():
    with open("template.html", encoding="utf-8") as f:
        template = f.read()

    with open("schools_data.json", encoding="utf-8") as f:
        data = json.load(f)

    raw_json = json.dumps(data, separators=(",", ":"), ensure_ascii=False)
    if PLACEHOLDER not in template:
        raise SystemExit(f"template.html is missing the {PLACEHOLDER} placeholder")

    out = template.replace(PLACEHOLDER, raw_json)
    with open("index.html", "w", encoding="utf-8", newline="\n") as f:
        f.write(out)

    print(f"index.html written: {len(data['schools'])} schools, "
          f"{len(out):,} bytes")


if __name__ == "__main__":
    main()
