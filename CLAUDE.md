# IHSA Postseason Scenario Explorer

Analysis tool supporting a proposal to the IHSA: separate public and private schools
in postseason brackets until the final 8, with travel-distance comparisons vs. the
current system.

## Files
- `index.html` — the built, self-contained explorer (deployed via Vercel from the
  GitHub repo mmason11/ihsa-scenario-explorer). Generated; do not hand-edit — see
  build pipeline below.
- `template.html` — the actual page source (markup, CSS, grouping/travel JS), with
  a placeholder in place of the embedded data: `const RAW = __RAW_DATA_JSON__;`.
- `schools_data.json` — the data that gets embedded: `{"schools": [...], "assign": {...}}`,
  one school per line for readable diffs. Each school carries `en` (base ISBE enrollment,
  pre-multiplier; `null` for the handful of schools added only via sport-roster matching —
  see `build_v2.py`'s `extra_rows`). Output of `build_v2.py`; hand-edits (e.g.
  resolving a review-list school's status) are also fine, then rerun `build_site.py`.
- `build_site.py` — substitutes `schools_data.json` into `template.html`'s placeholder,
  writes `index.html`. Run this any time `template.html` or `schools_data.json` changes.
- `prepare_data.py` — reads `source_data/IHSA_private_schools.xlsx`, normalizes
  public/private status, geocodes schools by city (offline `zipcodes` package),
  writes `schools_master.csv`.
- `new_sports.py` — actual IHSA sectional assignments transcribed from ihsa.org for
  FLGG, LAXB, LAXG, VBB, WPB, WPG, plus 2025 football playoff qualifiers by class
  (football currently removed from the UI; kept for the planned historical simulator).
- `build_v2.py` — matches assignment rosters to the master list, geocodes strays,
  emits `schools_data.json`.
- `scenario_engine.py` — Python mirror of the in-page grouping/travel logic.
- `schools_needing_review.csv` — header-only now; all 29 previously-unverified schools were
  researched and resolved July 2026 via `REVIEW_RESOLUTIONS` in `prepare_data.py` (kept there,
  not in the .xlsx, since the source workbook's Private? column is a cross-sheet VLOOKUP that
  openpyxl can't safely hand-edit — see the comment above that dict for the full rationale).
- `all_sports_summary.csv` — every sport/class at its recommended private-path count.

Pipeline: `prepare_data.py` → `schools_master.csv` → (+ `new_sports.py`) →
`build_v2.py` → `schools_data.json` → `build_site.py` → `index.html`.

## Key modeling notes
- Sports: SOB SOG VBG VBB BKB BKG BA SBG FLGG LAXB LAXG WPB WPG (cheer/dance/football removed).
- Current-system groupings are ACTUAL IHSA sectionals for FLGG/LAXB/LAXG/VBB/WPB/WPG;
  modeled (recursive geographic bisection) elsewhere. Proposed side is always modeled:
  publics get (8−P) sectional paths, privates get P; P recommended = round(8 × private share), 1–4.
- Travel = one-way straight-line miles to the host site (named IHSA host where actual,
  else most-central member school; per-sectional host overrides supported in the UI on
  both the Current and Proposed maps — to another member, any IHSA school, or a custom
  venue by street address, geocoded client-side via OpenStreetMap Nominatim). Locations
  are city-level ZIP centroids — Chicago-to-Chicago reads as ~0; road miles run ~15–25% higher.
- **Scenario Overrides tab** (in-browser only, `localStorage`, not part of the committed
  data). Three levers, all feeding live into the Scenario Explorer and Full Data tabs:
  - Per school, per sport: override enrollment; toggle the 1.65× multiplier (private
    schools only — applies by default to every private program unless waived, so this
    is a "what if waived/not waived" toggle, not an "is this school private" one); toggle
    the success factor (a direct one-class bump, e.g. 2A→3A, for a program that reached
    the state final 4 twice in the rolling three seasons before the one in question —
    public or private, independent of enrollment). Both toggles are manual stand-ins:
    neither is computed automatically because that needs Final-4/state-trophy history
    this tool doesn't have yet (same data gap as the football simulator below).
  - Per sport: edit a class's max-enrollment cutoff to reclassify every school in that sport
    at once. Cutoffs are IHSA's official published values (`CLASS_CUTOFFS` in `template.html`,
    current one-year cycle per ihsa.org/Schools/Enrollments-Classifications) for the 7 sports
    this tool classifies by enrollment (BA/BKB/BKG/SBG/VBG/SOB/SOG); doesn't account for co-op
    programs, which classify on combined enrollment rather than any one member's own figure.
  - Per school, per sport: manually move it to a different sectional — on the Current map for
    the 6 actual-assignment sports (FLGG/LAXB/LAXG/VBB/WPB/WPG), or on the Proposed map for
    whichever sport+class is currently selected in the top controls (Public/Private path
    names depend on that selection). Sectional-level only — regionals are recomputed
    geographically every run with no persistent identity, so there's no stable "regional N"
    to move a school into.

## Planned next steps
1. ~~Rebuild index.html as template + data build script instead of one embedded file.~~ Done:
   see `template.html` / `schools_data.json` / `build_site.py` above.
2. ~~Resolve the 29 review-list schools.~~ Done: see `REVIEW_RESOLUTIONS` in `prepare_data.py`.
3. Football historical simulator under the NEW playoff rules (8 classes of 32;
   1A–6A split into two 16-team brackets, 7A–8A seeded 1–32; seeding by record +
   at-large points; tiebreakers: most wins of defeated opponents, then head-to-head;
   round 1 hosted by higher seed, later rounds by whoever has hosted fewest, tie →
   higher seed). Compare vs. a private-separation variant using historical qualifier
   data (needed per team/season: class, wins, at-large points, opponents/results).
4. Possible upgrades: real school addresses, road-mileage routing, printable brackets.
