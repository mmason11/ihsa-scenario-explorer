"""
IHSA Public/Private Postseason Analysis - Step 1: Data prep & geocoding
Reads the compiled spreadsheet, normalizes school status, parses the host
city from the school name, and geocodes each city (offline, zip-code DB).
Outputs: schools_master.csv
"""
import pandas as pd
import re
import zipcodes

SRC = "source_data/IHSA_private_schools.xlsx"

SPORTS = {
    # fall
    "CCB": "Cross Country Boys", "CCG": "Cross Country Girls",
    "GOB": "Golf Boys", "GOG": "Golf Girls",
    "SOB": "Soccer Boys", "TNG": "Tennis Girls", "VBG": "Volleyball Girls",
    # winter
    "BKB": "Basketball Boys", "BKG": "Basketball Girls",
    "CHC": "Cheerleading", "DAC": "Dance", "SCB": "Scholastic Bowl", "WR": "Wrestling",
    # spring
    "BA": "Baseball", "SBG": "Softball Girls", "SOG": "Soccer Girls",
    "TNB": "Tennis Boys", "TRB": "Track Boys", "TRG": "Track Girls",
}

# City-name fixes: USPS city differs from common name, or parse edge cases
CITY_FIXES = {
    "Berwyn-Cicero": "Berwyn",
    "Bradley": "Bradley",
    "Carbondale": "Carbondale",
    "New Boston": "New Boston",
    "Sauk Village": "Sauk Village",
    "Chicago Heights": "Chicago Heights",
    "Cahokia": "Cahokia Heights",
    "Ford Heights": "Ford Heights",
    "Mt. Carmel": "Mount Carmel",
    "Mt. Zion": "Mt Zion",
    "Mt. Vernon": "Mount Vernon",
    "Mt. Olive": "Mount Olive",
    "Mt. Pulaski": "Mount Pulaski",
    "Mt. Prospect": "Mount Prospect",
    "Mt. Sterling": "Mount Sterling",
    "Mt. Morris": "Mount Morris",
    "Mt. Carroll": "Mount Carroll",
    "Mount Carroll": "Mount Carroll",
    "O'Fallon": "O Fallon",
    "LaGrange": "La Grange",
    "LaSalle": "La Salle",
    "St. Charles": "Saint Charles",
    "St. Anne": "Saint Anne",
    "St. Joseph": "Saint Joseph",
    "St. Elmo": "Saint Elmo",
    "St. Francisville": "Saint Francisville",
    "St. Libory": "New Athens",  # closest
    "East Peoria": "East Peoria",
    "Bartonville": "Peoria",           # Bartonville zips fold into Peoria
    "Cahokia": "East Saint Louis",
    "DeKalb": "Dekalb",
    "DeLand": "De Land",
    "DePue": "Depue",
    "DuQuoin": "Du Quoin",
    "Franklin Park-Northlake": "Franklin Park",
    "Johnsburg": "Mchenry",
    "LaGrange Park": "La Grange Park",
    "LaMoille": "La Moille",
    "LeRoy": "Le Roy",
    "McHenry": "Mchenry",
    "McLeansboro": "Mc Leansboro",
    "Norridge": "Harwood Heights",
    "Northfield": "Winnetka",
    "Summit": "Summit Argo",
    "West Prairie": "Colchester",      # West Prairie HS is in Sciota/Colchester area
    "Mount Zion": "Mt Zion",           # Mt. Zion zips
}


def parse_city(school: str) -> str:
    """School names look like 'City (Program Name)' or just 'City'."""
    m = re.match(r"^([^(]+?)\s*\(", school)
    city = m.group(1).strip() if m else school.strip()
    return CITY_FIXES.get(city, city)


def geocode_city(city: str):
    for name in (city, city.replace("St.", "Saint"), city.replace("Mt.", "Mount")):
        res = zipcodes.filter_by(city=name, state="IL")
        res = [r for r in res if r.get("lat")]
        if res:
            lats = [float(r["lat"]) for r in res]
            lons = [float(r["long"]) for r in res]
            return sum(lats) / len(lats), sum(lons) / len(lons)
    return None, None


def normalize_status(v):
    """
    'private'/'yes' -> private (non-boundaried private school)
    'no'            -> public non-boundaried (charter/magnet; multiplier applies
                       but NOT private for this proposal)
    0               -> public boundaried
    '?'/NaN         -> needs review; treated as public for bracket sims, flagged
    """
    if isinstance(v, str):
        v = v.strip().lower()
        if v in ("private", "yes"):
            return "private", False
        if v == "no":
            return "public_nonboundaried", False
        if v == "?":
            return "public_unverified", True
    if pd.isna(v):
        return "unclassified", True
    return "public", False


def main():
    df = pd.read_excel(SRC, sheet_name="All")
    rows = []
    cache = {}
    for _, r in df.iterrows():
        school = str(r["School"]).strip()
        if not school or school.lower() == "nan":
            continue
        status, needs_review = normalize_status(r["Private?"])
        city = parse_city(school)
        if city not in cache:
            cache[city] = geocode_city(city)
        lat, lon = cache[city]
        row = {
            "school": school,
            "city": city,
            "status": status,
            "is_private": status == "private",
            "needs_review": needs_review,
            "board_division": r["Board Division"],
            "district": r["District"],
            "lat": lat,
            "lon": lon,
        }
        for code in SPORTS:
            v = r.get(code)
            row[code] = str(v).strip() if pd.notna(v) and str(v).strip() else ""
        rows.append(row)

    out = pd.DataFrame(rows)
    out.to_csv("schools_master.csv", index=False)

    print(f"Schools processed: {len(out)}")
    print(f"Private: {out.is_private.sum()}")
    print(f"Public non-boundaried (charters etc.): {(out.status=='public_nonboundaried').sum()}")
    print(f"Needs review (? or blank): {out.needs_review.sum()}")
    missing = out[out.lat.isna()]
    print(f"\nFailed geocoding ({len(missing)}):")
    for s, c in zip(missing.school, missing.city):
        print(f"  {s}  ->  '{c}'")


if __name__ == "__main__":
    main()
