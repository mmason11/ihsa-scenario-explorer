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
  FLGG, LAXB, LAXG, VBB, WPB, WPG (single flat sectional list each — these are single-
  class sports), SOB (a class→sectional-list dict, since boys soccer has 3 independent
  classes each with their own ~8 sectionals — see below), plus 2025 football playoff
  qualifiers by class (football currently removed from the UI; kept for the planned
  historical simulator). Transcribed straight from ihsa.org's raw HTML bracket pages
  (`ihsa.org/data/{sport}/{class}pair.htm`) via regex, not WebFetch — WebFetch's small-
  model summarization drops the actual team rosters in favor of a results narrative
  (final scores, sectional champions), which is useless for reconstructing "who's in
  this sectional." The raw HTML is plain and reliable: `<H3>`/`<H4>` tags delimit
  Sectional/Regional sections, "Match N: TeamA s, TeamB s" lines name every team that
  played (winner or not) — every team appearing anywhere in a sectional's bracket is a
  member of it.
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
- Current-system groupings are ACTUAL IHSA sectionals for FLGG/LAXB/LAXG/VBB/WPB/WPG (single-
  class) and SOB (all 3 classes — added as a pilot for backfilling the rest); still modeled
  (recursive geographic bisection) for SOG/VBG/BKB/BKG/BA/SBG. `template.html`'s `realGroups(sport,
  class)` is the one place that reads `ASSIGN[sport]`, normalizing the two shapes (flat list for
  single-class, `{class: list}` dict for multi-class) — use it rather than touching `ASSIGN`
  directly. Real data has a coverage caveat vs. the classification-based field: e.g. for SOB/1A,
  12 schools classified 1A didn't field a team in the 2025 bracket (real participation varies
  year to year) and 2 schools played without a recorded SOB class — both fall out of the Current-
  side comparison in Full Data, which is expected, not a bug (confirmed by checking each one's
  `SOB` column in `schools_master.csv` directly). Proposed side is always modeled: publics get
  (8−P) sectional paths, privates get P; P recommended = round(8 × private share), 1–4.
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
  - Per school, per sport: manually move it to a different sectional — both Current and
    Proposed, tied to whichever sport+class is currently selected in the top controls (that's
    what determines the available target names). Current uses real sectional names where we
    have them (SOB + the 6 single-class sports) or "Sectional N" to match the modeled split
    otherwise; Proposed always uses "Public/Private path N". Sectional-level only — regionals
    are recomputed geographically every run with no persistent identity, so there's no stable
    "regional N" to move a school into.
- **Schools tab**: every school with a class in the sport picked up top (all classes at once,
  not filtered by the Class control) — enrollment, public/private, effective class, and inline
  1.65× multiplier / success-factor checkboxes that write into the same overrides as the
  Scenario Overrides tab. Sortable/searchable/CSV, same pattern as Full Data.

## Planned next steps
1. ~~Rebuild index.html as template + data build script instead of one embedded file.~~ Done:
   see `template.html` / `schools_data.json` / `build_site.py` above.
2. ~~Resolve the 29 review-list schools.~~ Done: see `REVIEW_RESOLUTIONS` in `prepare_data.py`.
3. Backfill real sectionals for the remaining modeled sports (SOG/VBG/BKB/BKG/BA/SBG — SOB
   done as a pilot, see above). 6 sports × 3-4 classes ≈ 18 more `{sport}/{class}pair.htm`
   pages to fetch and parse the same way; ~26 total across all 7 was the original estimate.
4. Football historical simulator under the NEW playoff rules (8 classes of 32;
   1A–6A split into two 16-team brackets, 7A–8A seeded 1–32; seeding by record +
   at-large points; tiebreakers: most wins of defeated opponents, then head-to-head;
   round 1 hosted by higher seed, later rounds by whoever has hosted fewest, tie →
   higher seed). Compare vs. a private-separation variant using historical qualifier
   data (needed per team/season: class, wins, at-large points, opponents/results). The
   Scenario Overrides tab's multiplier/success-factor toggles need this same Final-4/
   state-trophy history to compute automatically instead of being manual — worth
   pulling once, used for both.
5. Possible upgrades: road-mileage routing, printable brackets.
