"""
Actual IHSA state-series assignments for the added sports.
Sources (fetched July 2026):
- FLGG: 2025 Girls Flag Football pairings (ihsa.org/data/ffg/1pair.htm)
- LAXB: 2025-26 Boys Lacrosse brackets (ihsa.org/data/lcb/1bracket.htm)
- LAXG: 2025-26 Girls Lacrosse pairings (ihsa.org/data/lcg/1pair.htm)
- VBB : 2025-26 Boys Volleyball site assignments (ihsa.org/data/vbb/1assign.htm)
- WPB : 2024-25 Boys Water Polo pairings (archive)
- WPG : 2024-25 Girls Water Polo pairings (archive)
- FB  : 2025-26 Football playoff brackets, classes 1A-8A (ihsa.org/data/fb/Nbracket.htm)
- SOB : 2025 Boys Soccer pairings, classes 1A-3A (ihsa.org/data/sob/{1,2,3}pair.htm) — pilot
  for backfilling real sectionals in place of modeled ones for the sports still marked
  "modeled" in the tool. Parsed from the raw HTML bracket pages (regex over <H3>/<H4>
  section headers and "Match N: TeamA s, TeamB s" lines, not WebFetch's summarized text,
  which drops rosters in favor of a results narrative) — every team appearing anywhere in
  a sectional's bracket (winner or not) is a member of that sectional. 447/448 parsed team
  names matched schools_master.csv exactly; the one miss (Elgin (Harvest-Westminster))
  falls through to build_v2.py's normal new-school handling.
Names appear as printed by IHSA; coop suffixes in [brackets] are stripped by the matcher.
Single-class sports (FLGG/LAXB/LAXG/VBB/WPB/WPG) use one flat sectional list. Multi-class
sports (SOB) use a class -> sectional-list dict instead, since each class has its own
independent set of ~8 sectionals; build_v2.py and template.html both branch on
isinstance(secs, dict) to tell the two shapes apart.
"""

# sport -> list of (sectional_name, [schools]), OR for multi-class sports,
# sport -> {class: list of (sectional_name, [schools])}
ASSIGNMENTS = {
"FLGG": [
 ("Buffalo Grove Sectional", [
  "Buffalo Grove","Zion (Z.-Benton)","Elk Grove Village (E.G.)","Bensenville (Fenton)",
  "Northbrook (Glenbrook North)","Waukegan (H.S.)","Glenview (Glenbrook South)",
  "Lake Zurich","Deerfield (H.S.)","Mt. Prospect (Prospect)","Wheeling","Rolling Meadows",
  "Highland Park","Mundelein (Carmel)","Vernon Hills","Palatine (H.S.)","Palatine (Fremd)",
  "North Chicago","Arlington Heights (Hersey)","Mundelein (H.S.)","Lincolnshire (Stevenson)",
  "Arlington Heights (St. Viator)","Gurnee (Warren)","Barrington","Hoffman Estates (Conant)",
  "Schaumburg (H.S.)","Libertyville"]),
 ("Chicago (Lane) Sectional", [
  "Melrose Park (Walther Christian)","Chicago (Disney II)","Chicago (DePaul College Prep)",
  "Chicago (Senn)","Maywood (Proviso East)","Chicago (Schurz)","Park Ridge (Maine South)",
  "Chicago (Roosevelt)","Chicago (C. Academy)","Des Plaines (Maine West)","Chicago (CICS/Northtown)",
  "Skokie (Niles North)","Franklin Park-Northlake (Leyden)","Evanston (Twp.)",
  "Chicago (Northside)","Chicago (Lake View)","Skokie (Niles West)","Chicago (Rickover Naval Academy)",
  "Chicago (Lane)","Chicago (Taft)","Wilmette (Regina Dominican)","Chicago (Amundsen)",
  "Chicago (Resurrection)","Park Ridge (Maine East)","Wilmette (Loyola Academy)","Winnetka (New Trier)"]),
 ("Richton Park (Rich Township) Sectional", [
  "Crete (C.-Monee)","Chicago (C. Vocational)","Chicago (Agricultural Science)","Midlothian (Bremen)",
  "Tinley Park (Andrew)","Chicago (Harlan)","Chicago (Perspectives/Leadership)",
  "Orland Park (Sandburg)","Richton Park (Rich Township)","Palos Hills (Stagg)",
  "Blue Island (Eisenhower)","South Holland (Thornwood)","Chicago (Fenger)","Flossmoor (Homewood-F.)",
  "Chicago (Julian)","Oak Lawn (Community)","Chicago (Simeon)","Chicago (Noble/Butler)",
  "Chicago (Marist)","Chicago (Morgan Park)","Chicago Heights (Bloom Twp.)","Oak Lawn (Richards)",
  "Palos Heights (Shepard)","Chicago (Brooks)","Country Club Hills (Hillcrest)","Chicago (Mother McAuley)"]),
 ("Danville (H.S.) Sectional", [
  "Plainfield (Central)","Plainfield (North)","Romeoville (H.S.)","Joliet (Central)","Bolingbrook",
  "Plainfield (East)","Bradley (B.-Bourbonnais)","Danville (H.S.)","Peoria (H.S.)","Edwardsville (H.S.)",
  "Urbana (H.S.)","Mahomet (M.-Seymour)","Champaign (Centennial)","Belleville (East)",
  "Kankakee (Sr.)","Plainfield (South)","Oswego (H.S.)","Minooka","Yorkville (H.S.)","Joliet (West)",
  "Belleville (West)","Champaign (Central)","Mascoutah","Peoria (Manual)","Peoria (Richwoods)",
  "East St. Louis (Sr.)"]),
 ("South Elgin Sectional", [
  "Wheaton (W. Warrenville South)","Streamwood","Naperville (Central)","Aurora (East)",
  "Lisle (Benet Academy)","West Chicago (H.S.)","Glen Ellyn (Glenbard West)","Aurora (West Aurora)",
  "Hoffman Estates (H.S.)","St. Charles (East)","Addison (A. Trail)","Wheaton (North)",
  "Glen Ellyn (Glenbard South)","Geneva","South Elgin","Aurora (Rosary)","Carol Stream (Glenbard North)",
  "Oswego (East)","Bartlett","Naperville (North)","Elgin (Larkin)","St. Charles (North)",
  "Elmhurst (York)","Elgin (H.S.)","Elgin (St. Edward)","Roselle (Lake Park)","Wheaton (St. Francis)",
  "Lombard (Glenbard East)","Villa Park (Willowbrook)"]),
 ("Darien (Hinsdale South) Sectional", [
  "Chicago (Catalyst/Maria)","Chicago (Hancock)","Chicago (Lindblom)","Chicago (Noble/Johnson)",
  "Chicago (Phillips)","Chicago (Kelly)","Chicago (King)","Summit (Argo)","Chicago (Noble/Mansueto)",
  "Darien (Hinsdale South)","Chicago (Hubbard)","Downers Grove (South)","Hillside (Proviso West)",
  "Burbank (St. Laurence)","Chicago (Solorio Academy)","Chicago (Air Force Academy)",
  "Chicago (Perspectives/IIT Math & Science)","Chicago (C. Military Academy-Bronzeville)",
  "Elmhurst (Timothy Christian)","Chicago (Curie)","Chicago (Kenwood)","Downers Grove (North)",
  "Hinsdale (Central)","Chicago (Kennedy)","Chicago (Back of the Yards)","Burbank (Reavis)",
  "Chicago (Horizon/Southwest Chicago)","LaGrange (Lyons)"]),
 ("Chicago (Crane Medical Prep) Sectional", [
  "River Forest (Trinity)","Chicago (Juarez)","Berwyn-Cicero (Morton)","Chicago (Clark)",
  "Chicago (Jones)","Oak Park (Fenwick)","Chicago (Lincoln Park)","Chicago (De La Salle)",
  "Chicago (Ogden International)","Chicago (Noble/UIC)","Chicago (Westinghouse College Prep)",
  "Chicago (C. Hope Academy)","Chicago (North Lawndale Charter)","Chicago (Noble/Muchin)",
  "Chicago (Crane Medical Prep)","Chicago (Intrinsic Charter-Downtown Campus)","Chicago (Payton)",
  "Chicago (Christ the King)","Oak Park (O.P.-River Forest)","Chicago (North Grand)",
  "Chicago (Holy Trinity)","Chicago (St. Ignatius College Prep)","Chicago (Noble/Pritzker)",
  "Chicago (Noble/Bulls)","Chicago (Instituto Health Science Charter)","Chicago (Whitney Young)"]),
 ("McHenry Sectional", [
  "Carpentersville (Dundee-Crown)","Belvidere (North)","Antioch","Rockford (Boylan Catholic)",
  "Crystal Lake (Central)","Crystal Lake (South)","Huntley","Wauconda","Belvidere (H.S.)","McHenry",
  "Grayslake (North)","DeKalb","Fox Lake (Grant)","Cary (C.-Grove)","Rockford (Jefferson)",
  "Algonquin (Jacobs)","Round Lake","Harvard","Freeport (H.S.)","Rockford (Auburn)",
  "Rockton (Hononegah)","Grayslake (Central)","Rockford (Guilford)","Machesney Park (Harlem)",
  "Rockford (East)","Hampshire","Crystal Lake (Prairie Ridge)","Lake Villa (Lakes)"]),
],
"LAXB": [
 ("Wheaton (St. Francis) Sectional", [
  "Downers Grove (South)","Geneva","Aurora (Waubonsie Valley)","Lisle (Benet Academy)",
  "Wheaton (St. Francis)","St. Charles (North)","Aurora (Marmion Academy)",
  "Wheaton (W. Warrenville South)","St. Charles (East)","Naperville (Central)",
  "West Chicago (Wheaton Academy)","Naperville (North)","Batavia"]),
 ("Woodstock (Marian) Sectional", [
  "Huntley","Hampshire","Algonquin (Jacobs)","Crystal Lake (South)","Carpentersville (Dundee-Crown)",
  "Crystal Lake (Central)","Maple Park (Kaneland)","Barrington","McHenry","Wauconda",
  "Burlington (Central)","Cary (C.-Grove)","Crystal Lake (Prairie Ridge)"]),
 ("New Lenox (Lincoln-Way West) Sectional", [
  "New Lenox (Lincoln-Way West)","Dunlap","New Lenox (Providence Catholic)","Lockport (Twp.)",
  "Washington","Oswego (H.S.)","Lemont (H.S.)","Naperville (Neuqua Valley)","Normal (Community)",
  "Plainfield (North)","Tinley Park (Andrew)","Minooka"]),
 ("Oak Forest Sectional", [
  "Chicago (St. Ignatius College Prep)","Riverside (R.-Brookfield)","Chicago (Whitney Young)",
  "Chicago (Marist)","Chicago (Kenwood)","Chicago (Mt. Carmel)","Burbank (St. Laurence)",
  "LaGrange (Lyons)","Oak Forest","Chicago (Brother Rice)","Hinsdale (Central)","Chicago (St. Rita)",
  "LaGrange Park (Nazareth Academy)"]),
 ("Glenview (Glenbrook South) Sectional", [
  "Arlington Heights (St. Viator)","Mt. Prospect (Prospect)","Lincolnshire (Stevenson)",
  "Arlington Heights (Hersey)","Wheeling","Park Ridge (Maine South)","Buffalo Grove","Lake Zurich",
  "Glenview (Glenbrook South)","Palatine (H.S.)","Northbrook (Glenbrook North)","Palatine (Fremd)",
  "Rolling Meadows"]),
 ("Lake Forest (H.S.) Sectional", [
  "Lake Forest (H.S.)","Gurnee (Warren)","Mundelein (Carmel)","Fox Lake (Grant)","Deerfield (H.S.)",
  "Vernon Hills","Libertyville","Grayslake (North)","Highland Park","Lake Villa (Lakes)","Antioch",
  "Mundelein (H.S.)"]),
 ("Evanston (Twp.) Sectional", [
  "Wilmette (Loyola Academy)","Oak Park (O.P.-River Forest)","Chicago (Latin)","Evanston (Twp.)",
  "Chicago (St. Patrick)","Oak Park (Fenwick)","Chicago (Northside)","Winnetka (New Trier)",
  "Niles (Notre Dame)","Chicago (Lincoln Park)","Chicago (DePaul College Prep)","Chicago (Lane)",
  "Chicago (Taft)"]),
 ("Hoffman Estates (Conant) Sectional", [
  "Glen Ellyn (Glenbard West)","Hoffman Estates (Conant)","Hoffman Estates (H.S.)","Wheaton (North)",
  "Carol Stream (Glenbard North)","Elk Grove Village (E.G.)","Elmhurst (Timothy Christian)",
  "Elmhurst (York)","Elmhurst (IC Catholic)","Lombard (Montini)","South Elgin","Schaumburg (H.S.)",
  "Roselle (Lake Park)"]),
],
"LAXG": [
 ("Wilmette (Loyola Academy) Sectional", [
  "Chicago (DePaul College Prep)","Wheeling","Chicago (Payton)","Chicago (Northside)",
  "Wilmette (Regina Dominican)","Chicago (Lincoln Park)","Wilmette (Loyola Academy)",
  "Lincolnshire (Stevenson)","Chicago (Lane)","Northbrook (Glenbrook North)","Glenview (Glenbrook South)"]),
 ("Winnetka (New Trier) Sectional", [
  "Highland Park","Vernon Hills","Libertyville","Mundelein (H.S.)","Lake Forest (H.S.)",
  "Mundelein (Carmel)","Chicago (Latin)","Winnetka (New Trier)","Evanston (Twp.)","Deerfield (H.S.)"]),
 ("Crystal Lake (Central) Sectional", [
  "Buffalo Grove","Gurnee (Warren)","Hampshire","McHenry","Barrington","Palatine (Fremd)",
  "St. Charles (East)","Crystal Lake (Central)","Lake Zurich","Palatine (H.S.)"]),
 ("Huntley Sectional", [
  "Aurora (Rosary)","Oswego (H.S.)","Geneva","Streamwood","Burlington (Central)","Plainfield (East)",
  "Huntley","Naperville (Central)","Naperville (Neuqua Valley)","Naperville (North)",
  "Aurora (Metea Valley)"]),
 ("Chicago (Marist) Sectional", [
  "Riverside (R.-Brookfield)","Chicago (Kenwood)","Chicago (Marist)","Chicago (Whitney Young)",
  "Oak Park (Fenwick)","Burbank (St. Laurence)","Chicago (Mother McAuley)",
  "Oak Park (O.P.-River Forest)","Chicago (St. Ignatius College Prep)"]),
 ("O'Fallon (H.S.) Sectional", [
  "Normal (Community West)","Washington","Edwardsville (H.S.)","Minooka",
  "New Lenox (Lincoln-Way Central)","O'Fallon (H.S.)","Belleville (West)","Orland Park (Sandburg)",
  "Lockport (Twp.)","Dunlap"]),
 ("Hoffman Estates (H.S.) Sectional", [
  "Lombard (Montini)","Hoffman Estates (H.S.)","Schaumburg (H.S.)","Rolling Meadows",
  "Wheaton (St. Francis)","Wheaton (W. Warrenville South)","Elmhurst (York)",
  "Glen Ellyn (Glenbard West)","Hoffman Estates (Conant)","Downers Grove (North)","Lisle (Benet Academy)"]),
 ("Park Ridge (Maine South) Sectional", [
  "Arlington Heights (St. Viator)","River Forest (Trinity)","LaGrange (Lyons)",
  "Elk Grove Village (E.G.)","Chicago (Resurrection)","Chicago (Taft)","LaGrange Park (Nazareth Academy)",
  "Hinsdale (Central)","Park Ridge (Maine South)","Mt. Prospect (Prospect)","Arlington Heights (Hersey)"]),
],
"VBB": [
 ("Chicago (Lane) Sectional", [
  "Chicago (Amundsen)","Chicago (Christ the King)","Chicago (DePaul College Prep)","Chicago (Disney II)",
  "Chicago (Holy Trinity)","Chicago (Intrinsic Charter)","Chicago (Intrinsic Charter-Downtown Campus)",
  "Chicago (Kelvyn Park)","Chicago (Lake View)","Chicago (Lane)","Chicago (Latin)",
  "Chicago (Lycée Français de Chicago)","Chicago (Noble Street Charter)","Chicago (Noble/Bulls)",
  "Chicago (Noble/Golder)","Chicago (Noble/Muchin)","Chicago (Noble/Noble Academy)",
  "Chicago (Noble/Pritzker)","Chicago (North Grand)","Chicago (Ogden International)","Chicago (Payton)",
  "Chicago (Roosevelt)","Chicago (Schurz)","Chicago (Senn)","Chicago (Von Steuben)","Chicago (Wells)",
  "Chicago (Westinghouse College Prep)","Chicago (Whitney Young)","Chicago (Wolcott)"]),
 ("Chicago (Marist) Sectional", [
  "Blue Island (Eisenhower)","Calumet City (Thornton Fractional North)","Chicago (Agricultural Science)",
  "Chicago (Air Force Academy)","Chicago (Brooks)","Chicago (C. Hope Academy)",
  "Chicago (C. Military Academy-Bronzeville)","Chicago (Catalyst/Maria)","Chicago (Cristo Rey Jesuit)",
  "Chicago (De La Salle)","Chicago (Dyett)","Chicago (Horizon/Southwest Chicago)","Chicago (Jones)",
  "Chicago (Juarez)","Chicago (Kelly)","Chicago (Kenwood)","Chicago (Lindblom)","Chicago (Marist)",
  "Chicago (Mt. Carmel)","Chicago (Noble/Comer)","Chicago (Noble/Mansueto)","Chicago (Noble/UIC)",
  "Chicago (St. Ignatius College Prep)","Chicago (St. Rita)","Chicago (Tilden)","Chicago (Washington)",
  "Dolton (Thornridge)","Evergreen Park"]),
 ("Darien (Hinsdale South) Sectional", [
  "Aurora (East)","Aurora (Waubonsie Valley)","Bolingbrook","Darien (Hinsdale South)",
  "Downers Grove (North)","Downers Grove (South)","Glen Ellyn (Glenbard South)",
  "Glen Ellyn (Glenbard West)","Joliet (Catholic Academy)","Joliet (Central)","Joliet (West)",
  "Lemont (H.S.)","Lisle (Benet Academy)","Lockport (Twp.)","Lombard (Glenbard East)",
  "Lombard (Montini)","Minooka","Naperville (Central)","Naperville (Neuqua Valley)","Naperville (North)",
  "New Lenox (Providence Catholic)","Oswego (East)","Oswego (H.S.)","Plainfield (Central)",
  "Plainfield (East)","Plainfield (North)","Plainfield (South)","Romeoville (H.S.)",
  "Villa Park (Willowbrook)","Yorkville (H.S.)"]),
 ("Elgin (Larkin) Sectional", [
  "Aurora (Illinois Math and Science Academy)","Aurora (Marmion Academy)","Aurora (Metea Valley)",
  "Aurora (West Aurora)","Bartlett","Carol Stream (Glenbard North)","Geneva","South Elgin",
  "St. Charles (East)","St. Charles (North)","West Chicago (H.S.)","West Chicago (Wheaton Academy)",
  "Wheaton (North)","Wheaton (St. Francis)","Wheaton (W. Warrenville South)",
  "Belvidere (H.S.)","Belvidere (North)","Elgin (H.S.)","Elgin (Larkin)","Elgin (St. Edward)",
  "Freeport (H.S.)","Huntley","Machesney Park (Harlem)","Rockford (Auburn)","Rockford (Boylan Catholic)",
  "Rockford (East)","Rockford (Guilford)","Rockford (Jefferson)","Rockton (Hononegah)","Streamwood"]),
 ("Niles (Notre Dame) Sectional", [
  "Addison (A. Trail)","Arlington Heights (St. Viator)","Bensenville (Fenton)","Chicago (C. Academy)",
  "Chicago (CICS/Northtown)","Chicago (Horizon/Belmont)","Chicago (Northside)",
  "Chicago (Rickover Naval Academy)","Chicago (St. Patrick)","Chicago (Sullivan)","Chicago (Taft)",
  "Des Plaines (Maine West)","Elk Grove Village (E.G.)","Elmwood Park","Evanston (Beacon Academy)",
  "Evanston (Twp.)","Franklin Park-Northlake (Leyden)","Hoffman Estates (Conant)",
  "Hoffman Estates (H.S.)","Mt. Prospect (Prospect)","Niles (Notre Dame)","Norridge (Ridgewood)",
  "Palatine (Fremd)","Park Ridge (Maine East)","Park Ridge (Maine South)","Rolling Meadows",
  "Roselle (Lake Park)","Schaumburg (H.S.)","Skokie (Niles North)","Skokie (Niles West)"]),
 ("O'Fallon (H.S.) Sectional", [
  "Alton (Sr.)","Belleville (Althoff Catholic)","Belleville (East)","Belleville (West)","Bunker Hill",
  "Collinsville","Edwardsville (H.S.)","Edwardsville (Metro-East Lutheran)","Freeburg",
  "Glen Carbon (Father McGivney)","Granite City","Maryville (M. Christian)","O'Fallon (H.S.)",
  "Bradley (B.-Bourbonnais)","Chicago Heights (Bloom Twp.)","Chicago Heights (Marian)",
  "Country Club Hills (Hillcrest)","Crete (C.-Monee)","Flossmoor (Homewood-F.)",
  "Frankfort (Lincoln-Way East)","Kankakee (McNamara)","Kankakee (Sr.)","Midlothian (Bremen)",
  "New Lenox (Lincoln-Way Central)","New Lenox (Lincoln-Way West)","Oak Forest",
  "Richton Park (Rich Township)","Tinley Park (Andrew)","Tinley Park (H.S.)"]),
 ("Summit (Argo) Sectional", [
  "Berwyn-Cicero (Morton)","Burbank (Reavis)","Burbank (St. Laurence)","Chicago (Acero/Garcia)",
  "Chicago (Acero/Soto)","Chicago (Bogan)","Chicago (Brother Rice)","Chicago (Hancock)",
  "Chicago (Hubbard)","Chicago (Kennedy)","Chicago (Little Village)","Chicago (Solorio Academy)",
  "Elmhurst (IC Catholic)","Elmhurst (Timothy Christian)","Elmhurst (York)","Hillside (Proviso West)",
  "Hinsdale (Central)","LaGrange (Lyons)","LaGrange Park (Nazareth Academy)","Maywood (Proviso East)",
  "Melrose Park (Walther Christian)","Oak Lawn (Community)","Oak Lawn (Richards)","Oak Park (Fenwick)",
  "Oak Park (O.P.-River Forest)","Orland Park (Sandburg)","Palos Heights (Chicago Christian)",
  "Palos Heights (Shepard)","Palos Hills (Stagg)","Riverside (R.-Brookfield)","Summit (Argo)"]),
 ("Winnetka (New Trier) Sectional", [
  "Antioch","Arlington Heights (Hersey)","Barrington","Buffalo Grove",
  "Cary (Trinity Oaks Christian Academy)","Deerfield (H.S.)","Fox Lake (Grant)",
  "Glenview (Glenbrook South)","Grayslake (Central)","Grayslake (North)","Gurnee (Warren)",
  "Highland Park","Lake Forest (H.S.)","Lake Villa (Lakes)","Lake Zurich","Libertyville",
  "Lincolnshire (Stevenson)","Mundelein (Carmel)","Mundelein (H.S.)","North Chicago",
  "Northbrook (Glenbrook North)","Northfield (Christian Heritage Academy)","Palatine (H.S.)",
  "Round Lake","Vernon Hills","Waukegan (Cristo Rey St. Martin)","Waukegan (H.S.)","Wheeling",
  "Wilmette (Loyola Academy)","Winnetka (New Trier)","Zion (Z.-Benton)"]),
],
"WPB": [
 ("Barrington Sectional", [
  "Hoffman Estates (H.S.)","Rolling Meadows","McHenry","Elk Grove Village (E.G.)","Palatine (H.S.)",
  "Barrington","Arlington Heights (Hersey)","Schaumburg (H.S.)","Palatine (Fremd)","Hoffman Estates (Conant)"]),
 ("Chicago (Lane) Sectional", [
  "Chicago (Whitney Young)","Chicago (Latin)","Chicago (St. Ignatius College Prep)","Chicago (Jones)",
  "Chicago (Lane)","Chicago (Senn)","Chicago (Amundsen)","Chicago (Kenwood)"]),
 ("Elmhurst (York) Sectional", [
  "Berwyn-Cicero (Morton)","Chicago (Westinghouse College Prep)","Chicago (Northside)",
  "Franklin Park-Northlake (Leyden)","Elmhurst (York)","Oak Park (O.P.-River Forest)","Chicago (Taft)",
  "Oak Park (Fenwick)","St. Charles (North)","Chicago (St. Patrick)"]),
 ("Glenview (Glenbrook South) Sectional", [
  "Mt. Prospect (Prospect)","Des Plaines (Maine West)","Northbrook (Glenbrook North)",
  "Park Ridge (Maine East)","Winnetka (New Trier)","Glenview (Glenbrook South)",
  "Wilmette (Loyola Academy)","Evanston (Twp.)","Park Ridge (Maine South)","Skokie (Niles West)"]),
 ("LaGrange (Lyons) Sectional", [
  "Riverside (R.-Brookfield)","Chicago (Solorio Academy)","Chicago (Kennedy)","Summit (Argo)",
  "Chicago (Brother Rice)","Chicago (Curie)","Chicago (Mt. Carmel)","LaGrange (Lyons)",
  "Chicago (St. Rita)","Chicago (Goode STEM Academy)"]),
 ("Libertyville Sectional", [
  "Gurnee (Warren)","Lake Forest (H.S.)","Lincolnshire (Stevenson)","Mundelein (H.S.)","Vernon Hills",
  "Libertyville","Deerfield (H.S.)","Buffalo Grove","Highland Park"]),
 ("Naperville (North) Sectional", [
  "Orland Park (Sandburg)","Palos Heights (Shepard)","Naperville (North)","Naperville (Neuqua Valley)",
  "Hinsdale (Central)","Aurora (Waubonsie Valley)","Lockport (Twp.)","Naperville (Central)",
  "Aurora (Metea Valley)"]),
 ("New Lenox (Lincoln-Way West) Sectional", [
  "Chicago (Brooks)","Chicago (Agricultural Science)","Frankfort (Lincoln-Way East)",
  "New Lenox (Lincoln-Way Central)","Flossmoor (Homewood-F.)","Tinley Park (Andrew)",
  "Midlothian (Bremen)","New Lenox (Lincoln-Way West)","Bradley (B.-Bourbonnais)"]),
],
"WPG": [
 ("Barrington Sectional", [
  "Hoffman Estates (H.S.)","Rolling Meadows","Arlington Heights (Hersey)","Hoffman Estates (Conant)",
  "Schaumburg (H.S.)","Palatine (Fremd)","Palatine (H.S.)","Mt. Prospect (Prospect)","Barrington"]),
 ("Chicago (Lane) Sectional", [
  "Chicago (Kenwood)","Chicago (Amundsen)","Chicago (Senn)","Chicago (De La Salle)","Chicago (Jones)",
  "Chicago (Whitney Young)","Chicago (Lincoln Park)","Chicago (St. Ignatius College Prep)",
  "Chicago (Lane)","Chicago (Latin)"]),
 ("Elmhurst (York) Sectional", [
  "Franklin Park-Northlake (Leyden)","Berwyn-Cicero (Morton)","Elmhurst (York)","Oak Park (Fenwick)",
  "Elk Grove Village (E.G.)","Oak Park (O.P.-River Forest)","Chicago (Northside)","St. Charles (East)",
  "Chicago (Taft)"]),
 ("Glenview (Glenbrook South) Sectional", [
  "Evanston (Twp.)","Northbrook (Glenbrook North)","Des Plaines (Maine West)",
  "Glenview (Glenbrook South)","Winnetka (New Trier)","Skokie (Niles West)","Park Ridge (Maine South)",
  "Park Ridge (Maine East)"]),
 ("LaGrange (Lyons) Sectional", [
  "Summit (Argo)","Chicago (Agricultural Science)","LaGrange (Lyons)","Chicago (Curie)",
  "Chicago (Solorio Academy)","Chicago (Mother McAuley)","Riverside (R.-Brookfield)",
  "Oak Lawn (Richards)","Chicago (Kennedy)"]),
 ("Libertyville Sectional", [
  "Wheeling","Buffalo Grove","Lincolnshire (Stevenson)","Mundelein (H.S.)","Gurnee (Warren)",
  "Libertyville","Lake Forest (H.S.)","Vernon Hills","Deerfield (H.S.)"]),
 ("Naperville (North) Sectional", [
  "Naperville (Neuqua Valley)","Darien (Hinsdale South)","Naperville (North)","Hinsdale (Central)",
  "Aurora (Metea Valley)","Aurora (Waubonsie Valley)","Lockport (Twp.)","Naperville (Central)",
  "Orland Park (Sandburg)"]),
 ("New Lenox (Lincoln-Way West) Sectional", [
  "Palos Hills (Stagg)","Chicago (Brooks)","New Lenox (Lincoln-Way Central)","Midlothian (Bremen)",
  "Tinley Park (Andrew)","Frankfort (Lincoln-Way East)","Flossmoor (Homewood-F.)",
  "New Lenox (Lincoln-Way West)","Bradley (B.-Bourbonnais)"]),
],
"SOB": {
 "1A": [
  ("Effingham (H.S.) Sectional", [
   "Effingham (H.S.)", "Carlinville", "Rochester", "Teutopolis", "Altamont [Coop]", "Mt. Carmel", 
   "Pana [Coop]", "Vandalia", "Newton", "Raymond (Lincolnwood) [Coop]", "Piasa (Southwestern)", 
   "Salem", "Olney (Richland County)", "Robinson", "Effingham (St. Anthony)", "Staunton [Coop]", 
   "Greenville", "Springfield (Lutheran) [Coop]", "Virden (North Mac) [Coop]", "Litchfield", 
   "Hillsboro", 
  ]),
  ("Glen Carbon (Father McGivney) Sectional", [
   "Columbia", "Alton (Marquette)", "Glen Carbon (Father McGivney)", "Metropolis (Massac County)", 
   "Roxana", "Carlyle", "Lebanon", "Breese (Mater Dei)", "Pinckneyville", "Harrisburg [Coop]", 
   "Freeburg", "Anna (A.-Jonesboro) [Coop]", "Trenton (Wesclin)", "Wood River (East Alton-W.R.)", 
   "Maryville (M. Christian)", "Breese (Central)", "Vienna [Coop]", "Valmeyer", "Murphysboro", 
   "Waterloo (Gibault Catholic)", 
  ]),
  ("Johnsburg Sectional", [
   "Richmond (R.-Burton)", "Chicago (F.W. Parker)", "Chicago (C. Academy)", 
   "Northfield (Christian Heritage Academy)", "Skokie (Yeshiva)", "Morton Grove (MCC Academy)", 
   "Chicago (C. Math and Science Charter)", "Skokie (Ida Crown)", "Chicago (Holy Trinity)", 
   "Chicago (Marine Leadership Academy)", "Chicago (Noble Street Charter)", 
   "Chicago (ASPIRA/Business and Finance)", "Chicago (Alcott) [Coop]", "Chicago (Clemente)", 
   "Chicago (Rickover Naval Academy)", "Johnsburg", "Winnetka (North Shore Country Day)", 
   "Chicago (Lycée Français de Chicago)", "Deerfield (Rochelle Zell)", 
  ]),
  ("Westmont Sectional", [
   "Elmhurst (IC Catholic)", "Westmont", "Chicago (C. Hope Academy)", "Lisle (Sr.)", 
   "Chicago (Bogan)", "Bridgeview (Universal)", "Chicago (Richards)", 
   "Chicago (South Shore International College Prep)", "Chicago (Catalyst/Maria)", 
   "Chicago (Air Force Academy)", "Chicago (Horizon/Southwest Chicago)", 
   "Chicago (Horizon/McKinley)", "Lombard (Montini)", "Chicago (Noble/Rauner)", 
   "Chicago (Phoenix Military Academy)", "Villa Park (Islamic Foundation)", 
   "Chicago (Instituto Health Science Charter)", "Chicago (Daystar Academy)", 
   "Chicago (Noble/Golder)", "Lombard (College Prep)", 
  ]),
  ("Coal City Sectional", [
   "Coal City", "Herscher", "Manteno", "Palos Heights (Chicago Christian)", "Kankakee (McNamara)", 
   "Gilman (Iroquois West)", "St. Anne", "Clifton (Central)", "Hoopeston (H. Area) [Coop]", 
   "Watseka [Coop]", "Braidwood (Reed-Custer) [Coop]", "Momence", 
   "Chicago (Carver Military Academy)", "Crete (Illinois Lutheran)", "Joliet (Catholic Academy)", 
   "Beecher", "Yorkville (Y. Christian)", "South Holland (Unity Christian Academy)", "Peotone", 
   "Grant Park", 
  ]),
  ("Williamsville Sectional", [
   "Williamsville", "Fithian (Oakwood) [Coop]", "St. Joseph (S.J.-Ogden)", "Athens [Coop]", 
   "Monticello", "Argenta (A.-Oreana)", "Warrensburg (W.-Latham) [Coop]", "Mt. Pulaski", 
   "Pleasant Plains", "Decatur (St. Teresa)", "Arthur (A.-Lovington-Atwood-Hammond)", 
   "Macon (Meridian) [Coop]", "Riverton [Coop]", "Tolono (Unity)", 
   "Farmer City (Blue Ridge) [Coop]", "Urbana (University)", "Champaign (St. Thomas More)", 
   "Georgetown (G.-Ridge Farm)", "Danville (Schlarman)", "Fisher [Coop]", 
   "Bismarck (B.-Henning-Rossville-Alvin)", 
  ]),
  ("Chillicothe (Illinois Valley Central) Sectional", [
   "Rock Island (Alleman)", "Roanoke (R.-Benson) [Coop]", "Quincy (Notre Dame)", 
   "Peoria (P. Christian)", "Canton", "Macomb", "Glasford (Illini Bluffs) [Coop]", 
   "Abingdon (A.-Avon)", "Monmouth (M.-Roseville)", "Port Byron (Riverdale)", "Beardstown (H.S.)", 
   "Kewanee (H.S.)", "Princeton", "Stanford (Olympia)", 
   "Bloomington (Cornerstone Christian Academy)", "Chillicothe (Illinois Valley Central)", 
   "Peru (St. Bede)", "Normal (Calvary Christian Academy)", "Bloomington (Central Catholic)", 
   "Peoria (Manual)", 
  ]),
  ("Shabbona (Indian Creek) Sectional", [
   "Elgin (Harvest-Westminster)", "Byron", "Mendota", "Genoa (G.-Kingston)", "Serena", "Earlville", 
   "Somonauk [Coop]", "Hinckley (H.-Big Rock)", "Rockford (R. Christian)", "Woodstock (Marian)", 
   "Pecatonica [Coop]", "Rockford (Lutheran)", "Winnebago", "Marengo", "Stillman Valley", "Oregon", 
   "Poplar Grove (North Boone)", "Elgin (St. Edward)", "Sandwich", "Schaumburg (S. Christian)", 
   "Shabbona (Indian Creek)", 
  ]),
 ],
 "2A": [
  ("Mascoutah Sectional", [
   "Chatham (Glenwood)", "Waterloo (H.S.)", "Belleville (Althoff Catholic)", "Troy (Triad)", 
   "Jerseyville (Jersey)", "Taylorville", "Springfield (H.S.)", "Jacksonville (H.S.)", 
   "Mt. Vernon (H.S.)", "Mascoutah", "Carterville [Coop]", "Centralia (H.S.)", "Granite City", 
   "Carbondale (H.S.)", "Marion (H.S.)", "Highland", "Bethalto (Civic Memorial)", 
   "Springfield (Sacred Heart-Griffin)", 
  ]),
  ("Washington Sectional", [
   "Washington", "Urbana (H.S.)", "Normal (Community West)", "Mahomet (M.-Seymour)", "Lincoln", 
   "Metamora", "Normal (University)", "Rantoul [Coop]", "Charleston", "Mt. Zion", "Mattoon", 
   "Pekin", "Morton", "Bloomington (H.S.)", "Danville (H.S.)", "Champaign (Centennial)", 
   "Champaign (Central)", 
  ]),
  ("Darien (Hinsdale South) Sectional", [
   "Midlothian (Bremen)", "Lemont (H.S.)", "Darien (Hinsdale South)", "Chicago (Kennedy)", 
   "Chicago Heights (Marian)", "Chicago (University)", "Evergreen Park", "Chicago (Morgan Park)", 
   "Chicago (Brooks)", "New Lenox (Providence Catholic)", "Oak Lawn (Richards)", 
   "Chicago (Goode STEM Academy)", "Chicago (Agricultural Science)", "Oak Forest", 
   "Chicago (St. Rita)", "Chicago (Hubbard)", "Tinley Park (H.S.)", "Chicago (Washington)", 
   "Crete (C.-Monee)", 
  ]),
  ("Galesburg (H.S.) Sectional", [
   "Dunlap", "Kankakee (Sr.)", "Rock Island (H.S.)", "Aurora (Marmion Academy)", "Geneseo", 
   "Peoria (H.S.)", "Peoria (Richwoods)", "Galesburg (H.S.)", "Streator (Twp.) [Coop]", 
   "Aurora (Illinois Math and Science Academy)", "LaSalle (L.-Peru)", "Ottawa (Twp.)", 
   "Orion [Coop]", "East Peoria [Coop]", "Bartonville (Limestone)", "Sterling (H.S.)", "Plano", 
   "Morris [Coop]", "Aurora (Central Catholic)", "Dixon (H.S.)", 
  ]),
  ("Chicago (De La Salle) A Sectional", [
   "Chicago (De La Salle)", "Chicago (Solorio Academy)", "Elmhurst (Timothy Christian)", 
   "Chicago (Cristo Rey Jesuit)", "LaGrange Park (Nazareth Academy)", 
   "Chicago (Intrinsic Charter-Downtown Campus)", "Glen Ellyn (Glenbard South)", 
   "Chicago (Juarez)", "Riverside (R.-Brookfield)", "Chicago (Noble/Bulls)", 
   "Chicago (Back of the Yards)", "Chicago (Little Village)", "Chicago (Noble/Muchin)", 
   "Wheaton (St. Francis)", "Chicago (Noble/Mansueto)", "Chicago (Acero/Garcia)", 
   "Chicago (Noble/UIC)", "Chicago (Acero/Soto)", "Chicago (Kelly)", 
  ]),
  ("Chicago (De La Salle) B Sectional", [
   "Chicago (St. Patrick)", "Norridge (Ridgewood)", "Oak Park (Fenwick)", "Bensenville (Fenton)", 
   "Chicago (North Grand)", "Chicago (Disney II)", "Elmwood Park", "Chicago (Lake View)", 
   "Chicago (Westinghouse College Prep)", "Chicago (Schurz)", "Chicago (Northside)", 
   "Chicago (Noble/Pritzker)", "Chicago (Ogden International)", "Chicago (Roosevelt)", 
   "Chicago (Von Steuben)", "Chicago (Amundsen)", "Chicago (Intrinsic Charter)", 
   "Chicago (Payton)", "Chicago (Latin)", 
  ]),
  ("Geneva Sectional", [
   "Streamwood", "Rockford (Boylan Catholic)", "West Chicago (Wheaton Academy)", "Harvard", 
   "Rockford (East)", "Maple Park (Kaneland)", "Burlington (Central)", "Sycamore (H.S.)", 
   "Belvidere (H.S.)", "Rochelle", "Freeport (H.S.)", "Belvidere (North)", "Cary (C.-Grove)", 
   "Woodstock (North)", "Geneva", "Crystal Lake (Central)", "Woodstock (H.S.)", "Batavia", 
   "Crystal Lake (South)", "Crystal Lake (Prairie Ridge)", 
  ]),
  ("Grayslake (Central) Sectional", [
   "Grayslake (Central)", "Highland Park", "Grayslake (North)", "Mundelein (Carmel)", "Wheeling", 
   "Chicago (Sullivan)", "Waukegan (Cristo Rey St. Martin)", "Niles (Northridge Prep)", 
   "Chicago (Senn)", "North Chicago", "Lake Forest (H.S.)", "Lake Villa (Lakes)", 
   "Chicago (Mather)", "Antioch", "Arlington Heights (St. Viator)", "Deerfield (H.S.)", 
   "Chicago (CICS/Northtown)", "Wauconda", "Vernon Hills", 
  ]),
 ],
 "3A": [
  ("Arlington Heights (Hersey) Sectional", [
   "Northbrook (Glenbrook North)", "Arlington Heights (Hersey)", "Lincolnshire (Stevenson)", 
   "Barrington", "Zion (Z.-Benton)", "Fox Lake (Grant)", "Lake Zurich", "Libertyville", 
   "Glenview (Glenbrook South)", "Round Lake", "Mundelein (H.S.)", "Waukegan (H.S.)", 
   "Gurnee (Warren)", "Palatine (H.S.)", "Buffalo Grove", "Palatine (Fremd)", 
   "Mt. Prospect (Prospect)", 
  ]),
  ("South Elgin Sectional", [
   "St. Charles (North)", "Carpentersville (Dundee-Crown)", "South Elgin", "Bartlett", 
   "Rockford (Guilford)", "Machesney Park (Harlem)", "Hampshire", "Rockton (Hononegah)", 
   "St. Charles (East)", "Rockford (Jefferson)", "Algonquin (Jacobs)", "Rockford (Auburn)", 
   "Huntley", "McHenry", "DeKalb", "Elgin (Larkin)", "Elgin (H.S.)", 
  ]),
  ("Hinsdale (Central) Sectional", [
   "Berwyn-Cicero (Morton)", "Downers Grove (South)", "Burbank (St. Laurence)", "LaGrange (Lyons)", 
   "Chicago (Hancock)", "Chicago (Lindblom)", "Hinsdale (Central)", "Chicago (Whitney Young)", 
   "Summit (Argo)", "Burbank (Reavis)", "Chicago (Jones)", "Chicago (Curie)", 
   "Downers Grove (North)", "Oak Lawn (Community)", "Chicago (St. Ignatius College Prep)", 
   "Chicago (Kenwood)", "Chicago (Mt. Carmel)", 
  ]),
  ("Joliet (West) Sectional", [
   "New Lenox (Lincoln-Way West)", "Palos Hills (Stagg)", "New Lenox (Lincoln-Way Central)", 
   "Frankfort (Lincoln-Way East)", "Orland Park (Sandburg)", 
   "Calumet City (Thornton Fractional North) [Coop]", "Joliet (Central)", "Chicago (Brother Rice)", 
   "Blue Island (Eisenhower)", "Chicago Heights (Bloom Twp.)", "Palos Heights (Shepard)", 
   "Richton Park (Rich Township)", "Flossmoor (Homewood-F.)", "Harvey (Thornton) [Coop]", 
   "Chicago (Marist)", "Joliet (West)", "Tinley Park (Andrew)", 
  ]),
  ("Chicago (Taft) Sectional", [
   "Oak Park (O.P.-River Forest)", "Skokie (Niles West)", "Chicago (Lane)", 
   "Park Ridge (Maine South)", "Chicago (DePaul College Prep)", "Winnetka (New Trier)", 
   "Niles (Notre Dame)", "Maywood (Proviso East)", "Chicago (Prosser)", "Chicago (Taft)", 
   "Des Plaines (Maine West)", "Evanston (Twp.)", "Skokie (Niles North)", "Chicago (Lincoln Park)", 
   "Chicago (Noble/ITW Speer)", "Wilmette (Loyola Academy)", "Park Ridge (Maine East)", 
  ]),
  ("Schaumburg (H.S.) Sectional", [
   "West Chicago (H.S.)", "Franklin Park-Northlake (Leyden)", "Schaumburg (H.S.)", 
   "Hoffman Estates (H.S.)", "Glen Ellyn (Glenbard West)", "Carol Stream (Glenbard North)", 
   "Wheaton (W. Warrenville South)", "Wheaton (North)", "Roselle (Lake Park)", 
   "Hoffman Estates (Conant)", "Hillside (Proviso West)", "Elk Grove Village (E.G.)", 
   "Addison (A. Trail)", "Rolling Meadows", "Villa Park (Willowbrook)", "Lombard (Glenbard East)", 
   "Elmhurst (York)", 
  ]),
  ("Naperville (North) Sectional", [
   "Naperville (North)", "Lockport (Twp.)", "Naperville (Central)", "Aurora (West Aurora)", 
   "Plainfield (East)", "Oswego (H.S.)", "Plainfield (North)", "Romeoville (H.S.)", 
   "Aurora (East)", "Aurora (Waubonsie Valley)", "Bolingbrook", "Naperville (Neuqua Valley)", 
   "Lisle (Benet Academy)", "Aurora (Metea Valley)", "Plainfield (Central)", "Yorkville (H.S.)", 
   "Oswego (East)", 
  ]),
  ("Peoria (Notre Dame) Sectional", [
   "Collinsville", "O'Fallon (H.S.)", "Normal (Community)", "Minooka", 
   "Springfield (Southeast) [Coop]", "Belleville (West)", "Quincy (Sr.)", "Edwardsville (H.S.)", 
   "Belleville (East)", "Alton (Sr.)", "Plainfield (South)", "Bradley (B.-Bourbonnais)", 
   "East Moline (United)", "Decatur (MacArthur) [Coop]", "Peoria (Notre Dame)", "Moline (H.S.)", 
  ]),
 ],
},

}

# Football: class -> 32 playoff qualifiers (2025-26). No sectionals; seeded brackets.
FOOTBALL = {
"1A": ["Stockton","Galena (H.S.)","Heyworth","Princeville","Dwight","Clifton (Central)","Knoxville",
 "Rushville (R.-Industry)","Kewanee (Wethersfield)","Toulon (Stark County)","Mackinaw (Deer Creek)",
 "Chicago (Crane Medical Prep)","Lena (L.-Winslow)","Forreston","Gibson City (Melvin-Sibley)",
 "Ottawa (Marquette)","Hardin (Calhoun)","Villa Grove","Greenfield","Sesser (Valier)",
 "Casey (C.-Westfield)","Bridgeport (Red Hill)","Nokomis","Tuscola","Mt. Sterling (Brown County)",
 "Camp Point (Central)","Winchester","Athens","Carrollton","Dupo","Catlin (Salt Fork)","Fithian (Oakwood)"],
"2A": ["Taylor Ridge (Rockridge)","Carthage (Illini West)","Downs (Tri-Valley)","Chicago (Richards)",
 "Wilmington","Seneca","Port Byron (Riverdale)","Hamilton","El Paso (Gridley)","Chicago (Marshall)",
 "Sterling (Newman Central Catholic)","Colfax (Ridgeview)","Farmington","Lanark (Eastland)",
 "Aurora (A. Christian)","Erie","Johnston City","Trenton (Wesclin)","Maroa (M.-Forsyth)","Chester",
 "Flora","Nashville","Pana (H.S.)","Bismarck (B.-Henning-Rossville-Alvin)","Westville","Shelbyville",
 "DuQuoin (H.S.)","Carlinville","Arthur (A.-Lovington-Atwood-Hammond)","Marshall","Toledo (Cumberland)","Sullivan"],
"3A": ["Richmond (R.-Burton)","Poplar Grove (North Boone)","Aurora (Central Catholic)","Chicago (Noble/Rauner)",
 "Bloomington (Central Catholic)","Princeton","Monmouth (M.-Roseville)","Manteno","Byron","Oregon",
 "Pecatonica","Johnsburg","Kankakee (McNamara)","Herscher","Elmhurst (IC Catholic)","Chicago (C. Hope Academy)",
 "Williamsville","Hillsboro","Petersburg (PORTA)","Fairfield","Tolono (Unity)","Mt. Carmel","Monticello",
 "Paris","Vandalia","Christopher","Greenville","Stanford (Olympia)","St. Joseph (Ogden)","Benton",
 "Roxana","West Frankfort (Frankfort)"],
"4A": ["Lombard (Montini)","Chicago (Urban Prep/Bronzeville)","Peoria (Notre Dame)","Marengo","Dixon (H.S.)",
 "Woodstock (North)","Coal City","Sterling (H.S.)","Morris","Woodstock (H.S.)","Metamora",
 "Chicago (South Shore)","Macomb","Country Club Hills (Hillcrest)","Geneseo","Rochelle",
 "Olney (Richland County)","Jacksonville (H.S.)","Cahokia (H.S.)","Centralia (H.S.)","Breese (Central)",
 "Columbia","Freeburg","Highland","Carterville","Alton (Marquette)","Springfield (Sacred Heart-Griffin)",
 "Quincy (Notre Dame)","Rochester","Taylorville","Waterloo (H.S.)","Mt. Zion"],
"5A": ["Crystal Lake (Prairie Ridge)","Vernon Hills","Wheaton (St. Francis)","Chicago (Morgan Park)",
 "Chicago (King)","Chicago (Agricultural Science)","Chicago (Corliss)","Chicago (Lake View)",
 "Belvidere (North)","Chicago (Noble/Bulls)","Maple Park (Kaneland)","Lake Villa (Lakes)",
 "Cary (C.-Grove)","Sycamore (H.S.)","Wauconda","Chicago (St. Patrick)","Washington","Normal (University)",
 "Mahomet (M.-Seymour)","Marion (H.S.)","Kankakee (Sr.)","Lemont (H.S.)","New Lenox (Providence Catholic)",
 "Springfield (H.S.)","Oak Forest","Champaign (Centennial)","Bloomington (H.S.)","Mascoutah",
 "Peoria (H.S.)","Decatur (MacArthur)","Morton","Calumet City (Thornton Fractional North)"],
"6A": ["LaGrange Park (Nazareth Academy)","Rockton (Hononegah)","Wheaton (W. Warrenville South)",
 "Highland Park","Lake Zurich","Fox Lake (Grant)","Antioch","Glen Ellyn (Glenbard South)",
 "Burlington (Central)","Libertyville","Machesney Park (Harlem)","Chicago (Mather)",
 "Riverside (R.-Brookfield)","Rolling Meadows","Chicago (Kennedy)","Oak Park (Fenwick)",
 "Chatham (Glenwood)","Joliet (Catholic Academy)","East St. Louis (Sr.)","Plainfield (East)",
 "Normal (Community West)","South Holland (Thornwood)","Chicago (Goode STEM Academy)","Chicago (Simeon)",
 "Bradley (B.-Bourbonnais)","Palos Heights (Shepard)","Oak Lawn (Community)","Burbank (St. Laurence)",
 "Crete (C.-Monee)","Quincy (Sr.)","Dunlap","Pekin"],
"7A": ["Oak Lawn (Richards)","Edwardsville (H.S.)","Arlington Heights (Hersey)","Chicago (Payton)",
 "Rockford (Guilford)","Chicago (St. Rita)","New Lenox (Lincoln-Way Central)","Burbank (Reavis)",
 "Lombard (Glenbard East)","West Chicago (H.S.)","Batavia","Hoffman Estates (H.S.)",
 "Carol Stream (Glenbard North)","Moline (H.S.)","Tinley Park (Andrew)","Yorkville (H.S.)",
 "Glen Ellyn (Glenbard West)","Villa Park (Willowbrook)","Downers Grove (North)","Mt. Prospect (Prospect)",
 "New Lenox (Lincoln-Way West)","Chicago (Lincoln Park)","Chicago (Kenwood)","Chicago (Prosser)",
 "St. Charles (North)","East Moline (United)","Mundelein (Carmel)","Normal (Community)",
 "Chicago (Brother Rice)","Rockford (Jefferson)","Algonquin (Jacobs)","Addison (A. Trail)"],
"8A": ["Chicago (Mt. Carmel)","Wilmette (Loyola Academy)","Belleville (East)","Aurora (West Aurora)",
 "Frankfort (Lincoln-Way East)","Chicago (Whitney Young)","Palatine (H.S.)","Lincolnshire (Stevenson)",
 "Palatine (Fremd)","Huntley","LaGrange (Lyons)","Elmhurst (York)","Bolingbrook","Gurnee (Warren)",
 "Winnetka (New Trier)","Oswego (East)","Barrington","Elgin (H.S.)","Glenview (Glenbrook South)",
 "Minooka","Chicago (Curie)","Flossmoor (Homewood-F.)","Orland Park (Sandburg)","Lockport (Twp.)",
 "Park Ridge (Maine South)","Downers Grove (South)","Hinsdale (Central)","South Elgin","Chicago (Lane)",
 "Chicago (Perspectives/Leadership)","Oswego (H.S.)","Naperville (North)"],
}
