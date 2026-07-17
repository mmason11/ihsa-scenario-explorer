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
- `new_sports.py` — actual IHSA sectional assignments transcribed from ihsa.org for every
  sport the tool tracks: FLGG, LAXB, LAXG, VBB, WPB, WPG (single flat sectional list each —
  these are single-class sports) and SOB/SOG/VBG/BKB/BKG/BA/SBG (a class→sectional-list dict
  each, since these are multi-class — each class has its own independent ~8 sectionals —
  see below), plus 2025 football playoff qualifiers by class (football currently removed
  from the UI; kept for the planned historical simulator). Transcribed straight from
  ihsa.org's raw HTML bracket pages (`ihsa.org/data/{sport}/{class}pair.htm`) via regex, not
  WebFetch — WebFetch's small-model summarization drops the actual team rosters in favor of
  a results narrative (final scores, sectional champions), which is useless for
  reconstructing "who's in this sectional." The raw HTML is plain and reliable: `<H3>`/`<H4>`
  tags delimit Sectional/Regional sections, and result lines name every team that played
  (winner or not) — every team appearing anywhere in a sectional's bracket is a member of
  it. Two result-line formats: "Match/Game N: TeamA s, TeamB s" (soccer/basketball/baseball/
  softball) and volleyball's "Match N: TeamA d. TeamB, set-scores" — see `parse_pairings.py`.
- `parse_pairings.py` — parses a saved bracket page into `new_sports.py`'s `ASSIGNMENTS` shape.
  Not part of the main pipeline; a standalone tool re-run when a new season's pairings post
  (usage/fetch command in its docstring).
- `build_v2.py` — matches assignment rosters to the master list, geocodes strays, embeds
  `state_finalists.json` per school as `fin` (see below), emits `schools_data.json`.
- `state_finalists.json` — `{sport: {year: [schools that reached the state final 4]}}` for
  the 7 enrollment-classified sports, 2022-23 through 2025-26 (the years needed for the
  rolling-three-year success-factor window, current and next season — see template.html's
  `SF_WINDOW_CUR`/`SF_WINDOW_NEXT`). Output of `pull_state_finalists.py`.
- `pull_state_finalists.py` — parses saved bracket pages' "State Final Tournament" section
  (reuses `parse_pairings.py`'s format detection) into `state_finalists.json`. Not part of
  the main pipeline; a standalone tool re-run once a year as the window rolls forward
  (fetch command + full instructions in its docstring) — same spirit as `parse_pairings.py`,
  and in fact pulls from the very same bracket pages plus one prior-season archive
  (`ihsa.org/archive/{sport}/{year}/{class}pair.htm`, confirmed to go back to at least
  2021-22) for the two years before what's on the live site.
- `classifications_flags.json` — `{school: {sport: {"class": "2A", "flag": "coop"|
  "waived"|"multiplier"|"success"|"playup"|null}}}` for SOB/VBG/BKB/BKG (fall+winter
  cycle pages only — no spring page has been found posted or archived for the
  2025-26 cycle, so BA/SBG/SOG aren't covered). Output of `pull_classifications.py`;
  `build_v2.py` uses it to correct `schools_master.csv`'s class value where it
  differs (co-op combined enrollment isn't in that column) and embeds the flag
  itself per school as `flg`.
- `pull_classifications.py` — parses IHSA's color-coded School Classifications pages
  (ihsa.org/Schools/Enrollments-Classifications) into `classifications_flags.json`.
  Not part of the main pipeline; re-run each cycle (fetch commands in its docstring).
  This is the authoritative source for things this tool previously only guessed —
  co-op status, per-program multiplier waiver, and IHSA's own "success formula" flag
  — cross-validated against `state_finalists.json`'s independently-reconstructed
  success-factor calls (Peoria (Notre Dame): both agree exactly on SOB and BKG) and
  against the class values already in `schools_master.csv` (97.9% agreement; the 42
  disagreements are mostly co-op, the rest are real errors in the older data, now
  corrected by this source taking precedence).
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
- Current-system groupings are ACTUAL IHSA sectionals for every sport the tool tracks — no
  sport falls back to modeled (recursive geographic bisection) grouping anymore, though the
  fallback code path still exists in `template.html`'s `realGroups(sport, class)` (the one
  place that reads `ASSIGN[sport]`, normalizing the two shapes: flat list for the 6 single-
  class sports FLGG/LAXB/LAXG/VBB/WPB/WPG, `{class: list}` dict for the 7 multi-class sports
  SOB/SOG/VBG/BKB/BKG/BA/SBG — use it rather than touching `ASSIGN` directly) in case a future
  sport needs it. Real data has a coverage caveat vs. the classification-based field: e.g. for
  SOB/1A, 12 schools classified 1A didn't field a team in the 2025 bracket (real participation
  varies year to year) and 2 schools played without a recorded SOB class — both fall out of
  the Current-side comparison in Full Data, which is expected, not a bug (confirmed by
  checking each one's `SOB` column in `schools_master.csv` directly; similar small gaps exist
  for the other 6 sports — see `new_sports.py`'s docstring for exact counts). Proposed side is
  always modeled by design (that's the whole point of the proposal): publics get
  (8−P) sectional paths, privates get P; P recommended = round(8 × private share), 1–4.
- Travel = one-way straight-line miles to the host site (named IHSA host where actual,
  else most-central member school; per-sectional host overrides supported in the UI on
  both the Current and Proposed maps — to another member, any IHSA school, or a custom
  venue by street address, geocoded client-side via OpenStreetMap Nominatim). Locations
  are city-level ZIP centroids — Chicago-to-Chicago reads as ~0; road miles run ~15–25% higher.
- **Success factor** (private-only, like the multiplier — a public school never gets the
  checkbox regardless of history): a direct one-class bump (e.g. 2A→3A) for a private program
  that reached the state final 4 twice in the rolling three seasons before the one in
  question. `autoSuccessFactor()` prefers IHSA's own published "success formula" flag
  (`classifications_flags.json`, SOB/VBG/BKB/BKG only — checkbox shows "(auto)") over
  reconstructing it from `state_finalists.json`'s history (used for BA/SBG/SOG, and always
  for the *next-year* projection, since the flag is a same-year snapshot); still overridable
  per school. Validated by hand against Peoria (Notre Dame) boys soccer (2022-23 champion,
  2023-24 runner-up → 3A this year, exactly matching IHSA's own "success" flag; only 2023-24
  survives into next year's window → projected to drop to 2A) before wiring in.
  `effectiveClass()` is careful not to double-bump: the transcribed base class already
  includes any real success-factor bump, so it's returned untouched unless something
  *actually* changed (enrollment/multiplier/cutoff override, or an explicit success-factor
  override that disagrees with the auto-computed value).
- **Multiplier waiver**: same idea — `officialMultState()` prefers IHSA's own published
  waived/multiplier flag for SOB/VBG/BKB/BKG, falling back to "every private program is
  multiplied unless the user says otherwise" for BA/SBG/SOG and anywhere else the flag data
  doesn't cover. Cross-validating this data against the class values already in
  `schools_master.csv` also caught and fixed 28 real errors (mostly co-op combined
  enrollment, e.g. Batavia SOB was recorded as 2A but is actually 3A) — most of the
  previously-unexplained "actual class higher than enrollment alone predicts" cases turned
  out to be exactly this.
- **Scenario Overrides tab** (in-browser only, `localStorage`, not part of the committed
  data). Two per-school, per-sport levers, feeding live into the Scenario Explorer and Full
  Data tabs: override enrollment; toggle the 1.65× multiplier (applies by default to every
  private program unless waived, so this is a "what if waived/not waived" toggle, not an "is
  this school private" one, and is distinct from the global multiplier *value* lever on the
  Schools tab below); toggle the success factor (see above). Also: manually move a school to
  a different sectional — both Current and Proposed, tied to whichever sport+class is
  currently selected in the top controls (that's what determines the available target names).
  Current uses real sectional names where we have them (every sport now — see above) or
  "Sectional N" as a fallback if a future sport lacks real data; Proposed always uses
  "Public/Private path N". Same override, two entry points: the school-search panel here, or
  a "Move to" dropdown directly in each roster row on the Scenario Explorer tab's sectional
  detail panel (`renderDetail()`) — added after initial feedback that burying this in a
  separate tab, away from the map you're actually looking at, wasn't discoverable. Sectional-
  level only — regionals are recomputed geographically every run with no persistent identity,
  so there's no stable "regional N" to move a school
  into.
- **Schools tab**: every school with a class in the sport picked up top (all classes at once,
  not filtered by the Class control) — enrollment, adjusted enrollment (post-multiplier/
  override, via `effectiveEnrollment`), public/private, effective class, IHSA's own published
  flag where available (co-op/waived/multiplier/success/played-up — `classifications_flags.json`,
  SOB/VBG/BKB/BKG only), expected class *next* year (`nextYearClass()` — enrollment at the
  official 1.65× regardless of any scenario overrides in effect, plus next year's rolling
  success-factor window; a projection, since it can't know next year's actual enrollment or
  results), and inline multiplier/success-factor checkboxes that write into the same overrides
  as the Scenario Overrides tab. Filterable by
  type and class, sortable/searchable/CSV, same pattern as Full Data. Also hosts two sport-
  wide/tool-wide levers (moved here from Scenario Overrides since they aren't per-school): a
  classification-cutoff editor (slider + number input per class boundary, reclassifying the
  whole field for the selected sport at once) and a multiplier-*value* editor (slider + number
  input, default 1.65×, changes the multiplier itself — not just who's waived — across every
  private school/sport at once, e.g. "what would 1.5× or 2× do instead"). Both are official-
  values-per-sport (`CLASS_CUTOFFS`, current one-year cycle per ihsa.org/Schools/Enrollments-
  Classifications, for the 7 sports this tool classifies by enrollment: BA/BKB/BKG/SBG/VBG/
  SOB/SOG) unless overridden; doesn't account for co-op programs, which classify on combined
  enrollment rather than any one member's own figure. A class summary table (schools/public/
  private per class, using effective class) rounds out the tab, all driven by the same sport
  picker in the top controls.

## Planned next steps
1. ~~Rebuild index.html as template + data build script instead of one embedded file.~~ Done:
   see `template.html` / `schools_data.json` / `build_site.py` above.
2. ~~Resolve the 29 review-list schools.~~ Done: see `REVIEW_RESOLUTIONS` in `prepare_data.py`.
3. ~~Backfill real sectionals for the remaining modeled sports.~~ Done: SOG/VBG/BKB/BKG/BA/SBG
   all transcribed the same way as the SOB pilot — every sport the tool tracks now uses real
   IHSA data. See `new_sports.py`'s docstring and `parse_pairings.py`.
4. ~~Automate the success-factor toggle from real Final-4/state-trophy history.~~ Done: see
   `pull_state_finalists.py` / `state_finalists.json` above. The multiplier's waiver toggle
   is a different, unrelated question (which programs have petitioned for a waiver) that
   isn't public data anywhere we've found — still manual.
5. Football historical simulator under the NEW playoff rules (8 classes of 32;
   1A–6A split into two 16-team brackets, 7A–8A seeded 1–32; seeding by record +
   at-large points; tiebreakers: most wins of defeated opponents, then head-to-head;
   round 1 hosted by higher seed, later rounds by whoever has hosted fewest, tie →
   higher seed). Compare vs. a private-separation variant using historical qualifier
   data (needed per team/season: class, wins, at-large points, opponents/results) —
   `state_finalists.json`'s final-4 data is a start but this needs full season records,
   not just who reached state finals.
6. Possible upgrades: road-mileage routing, printable brackets.
