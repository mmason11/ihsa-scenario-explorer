"""
IHSA Public/Private Postseason Analysis - Step 2: Scenario engine

Models the state series as: regionals -> sectionals -> (sectional champs = final 8).

CURRENT SYSTEM: all schools in a class (public + private) are grouped
geographically into 8 sectionals; each sectional is subdivided into regionals.

PROPOSED SYSTEM: public schools get P sectionals, private schools get (8-P)
sectionals of their own, so no public/private matchup can occur before the
final 8. P is a scenario parameter (e.g. 7 public + 1 private).

Grouping method: recursive geographic bisection - split the field at the
median along its wider axis (lon/lat), recursively, producing balanced,
contiguous groups. Deterministic and mirrors how brackets are drawn.

Travel proxy: one-way distance from each school to its group's centroid
(approximates travel to a centrally-seeded host site).
"""
import math
import pandas as pd
import numpy as np

MASTER = "schools_master.csv"


def haversine_mi(lat1, lon1, lat2, lon2):
    R = 3958.8
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def bisect_groups(df, n_groups):
    """Recursively split schools into n_groups balanced geographic groups."""
    if n_groups <= 1 or len(df) <= 1:
        return [df]
    n_left = n_groups // 2
    n_right = n_groups - n_left
    frac = n_left / n_groups
    # split along the axis with more geographic spread (lon scaled by cos(lat))
    lat_span = df.lat.max() - df.lat.min()
    lon_span = (df.lon.max() - df.lon.min()) * math.cos(math.radians(df.lat.mean()))
    axis = "lat" if lat_span >= lon_span else "lon"
    d = df.sort_values(axis)
    k = round(len(d) * frac)
    k = max(1, min(len(d) - 1, k))
    return bisect_groups(d.iloc[:k], n_left) + bisect_groups(d.iloc[k:], n_right)


def group_metrics(groups, level_name):
    """Distance from each school to its group centroid."""
    recs = []
    for gi, g in enumerate(groups):
        if len(g) == 0:
            continue
        clat, clon = g.lat.mean(), g.lon.mean()
        for _, r in g.iterrows():
            recs.append({
                "school": r.school, "is_private": r.is_private,
                f"{level_name}_id": gi,
                f"{level_name}_mi": haversine_mi(r.lat, r.lon, clat, clon),
            })
    return pd.DataFrame(recs)


def simulate(field, n_sectionals, regional_size=5, label=""):
    """Assign a field of schools to sectionals + regionals; return per-school travel."""
    if len(field) == 0:
        return pd.DataFrame()
    n_sec = min(n_sectionals, len(field))
    sectionals = bisect_groups(field, n_sec)
    sec_m = group_metrics(sectionals, "sectional")
    reg_rows = []
    for si, sec in enumerate(sectionals):
        n_reg = max(1, round(len(sec) / regional_size))
        regionals = bisect_groups(sec, n_reg)
        m = group_metrics(regionals, "regional")
        m["sectional_id"] = si
        reg_rows.append(m[["school", "regional_mi"]])
    reg_m = pd.concat(reg_rows)
    out = sec_m.merge(reg_m, on="school")
    out["scenario"] = label
    return out


def summarize(m, who=""):
    if len(m) == 0:
        return {}
    return {
        "group": who, "teams": len(m),
        "reg_mean": round(m.regional_mi.mean(), 1),
        "reg_max": round(m.regional_mi.max(), 1),
        "sec_mean": round(m.sectional_mi.mean(), 1),
        "sec_max": round(m.sectional_mi.max(), 1),
        "sec_over75": int((m.sectional_mi > 75).sum()),
        "sec_over150": int((m.sectional_mi > 150).sum()),
    }


def run_sport_class(df, sport, klass, private_sectionals=1, total_sectionals=8):
    field = df[(df[sport] == klass) & df.lat.notna()].copy()
    priv = field[field.is_private]
    pub = field[~field.is_private]

    results = {}
    # CURRENT: everyone mixed, 8 sectionals
    cur = simulate(field, total_sectionals, label="current")
    results["current_all"] = summarize(cur, "all")
    results["current_private"] = summarize(cur[cur.is_private], "private")
    results["current_public"] = summarize(cur[~cur.is_private], "public")

    # PROPOSED: publics get (total - private_sectionals), privates get the rest
    pub_sim = simulate(pub, total_sectionals - private_sectionals, label="proposed_public")
    prv_sim = simulate(priv, private_sectionals, label="proposed_private")
    results["proposed_public"] = summarize(pub_sim, "public")
    results["proposed_private"] = summarize(prv_sim, "private")

    detail = pd.concat([cur, pub_sim, prv_sim], ignore_index=True)
    return field, results, detail


if __name__ == "__main__":
    df = pd.read_csv(MASTER)
    sport = "SOB"  # Boys Soccer
    print(f"=== BOYS SOCCER scenario comparison (8 sectionals; privates get 1) ===\n")
    for klass in ["1A", "2A", "3A"]:
        field, res, detail = run_sport_class(df, sport, klass, private_sectionals=1)
        n_priv = field.is_private.sum()
        print(f"--- {klass}: {len(field)} teams ({n_priv} private, {len(field)-n_priv} public) ---")
        rows = pd.DataFrame([
            {**{"scenario": k}, **v} for k, v in res.items() if v
        ])
        print(rows.to_string(index=False))
        # worst-hit private schools under proposal
        worst = (detail[detail.scenario == "proposed_private"]
                 .nlargest(5, "sectional_mi")[["school", "regional_mi", "sectional_mi"]])
        print("\nFarthest private-school sectional travel under proposal:")
        print(worst.round(1).to_string(index=False))
        print()
