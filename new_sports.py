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
Names appear as printed by IHSA; coop suffixes in [brackets] are stripped by the matcher.
"""

# sport -> list of (sectional_name, [schools])
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
