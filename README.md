# IHSA Postseason Scenario Explorer

Interactive analysis of a proposed IHSA state-series change separating public and
private schools until the final 8, with travel-distance comparisons against the
current system across 16 sports.

- Fully static, self-contained single page (`index.html`) — no build step, no dependencies.
- Current-system groupings use actual IHSA sectional assignments for flag football,
  lacrosse, boys volleyball, and water polo; other sports use modeled geographic grouping.
- Travel = one-way straight-line miles to the host site (named IHSA host where known,
  otherwise the most centrally located school in the group). Locations are city-level.
