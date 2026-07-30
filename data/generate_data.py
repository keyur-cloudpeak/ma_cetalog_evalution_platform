"""
Dummy data generator for the M&A Catalog Valuation Workbench.
Run once to produce the JSON files consumed by app.py.
All figures are synthetic / illustrative only.
"""
import json
import random
from pathlib import Path

random.seed(42)
OUT = Path(__file__).parent

# ---------------------------------------------------------------------------
# 1. Catalog search universe (Screen 1)
# ---------------------------------------------------------------------------
catalog_options = {
    "artists": ["Shakira", "Karol G", "Bad Bunny", "Harry Styles", "Camila Cabello",
                "Manuel Turizo", "Rauw Alejandro", "Sebastian Yatra"],
    "labels": ["CHI Records", "RCA Records", "Columbia Records", "Arista Records",
               "Nashville West Records", "Sony Music Latin"],
}
with open(OUT / "catalog_options.json", "w") as f:
    json.dump(catalog_options, f, indent=2)

# ---------------------------------------------------------------------------
# 2. Ambiguity resolution matches (Screen 2)
# ---------------------------------------------------------------------------
ambiguity_matches = {
    "CHI Records": [
        {"id": "LBL001", "name": "CHI Records", "confidence": "High", "track_count": 482, "recommended": True},
        {"id": "LBL002", "name": "CHI Records MC", "confidence": "Medium", "track_count": 61, "recommended": False},
        {"id": "LBL003", "name": "CHI Power Records", "confidence": "Low", "track_count": 19, "recommended": False},
    ],
    "Shakira": [
        {"id": "ART001", "name": "Shakira", "confidence": "High", "track_count": 214, "recommended": True},
        {"id": "ART002", "name": "Shakira ft.", "confidence": "Low", "track_count": 8, "recommended": False},
    ],
}

for i, artist in enumerate(catalog_options["artists"]):
    if artist not in ambiguity_matches:
        ambiguity_matches[artist] = [
            {"id": f"ART{(i*2+3):03d}", "name": artist, "confidence": "High", "track_count": random.randint(50, 300), "recommended": True},
            {"id": f"ART{(i*2+4):03d}", "name": f"{artist} ft.", "confidence": "Low", "track_count": random.randint(5, 50), "recommended": False},
        ]

for i, label in enumerate(catalog_options["labels"]):
    if label not in ambiguity_matches:
        ambiguity_matches[label] = [
            {"id": f"LBL{(i*3+4):03d}", "name": label, "confidence": "High", "track_count": random.randint(100, 600), "recommended": True},
            {"id": f"LBL{(i*3+5):03d}", "name": f"{label} MC", "confidence": "Medium", "track_count": random.randint(20, 90), "recommended": False},
            {"id": f"LBL{(i*3+6):03d}", "name": f"{label} Power", "confidence": "Low", "track_count": random.randint(5, 30), "recommended": False},
        ]
with open(OUT / "ambiguity_matches.json", "w") as f:
    json.dump(ambiguity_matches, f, indent=2)

# ---------------------------------------------------------------------------
# 3. Territories (Screen 3)
# ---------------------------------------------------------------------------
territories = {
    "regions": {
        "Central America": ["Mexico", "Guatemala", "Honduras", "El Salvador", "Costa Rica", "Panama"],
        "South America": ["Colombia", "Argentina", "Chile", "Peru", "Ecuador", "Brazil"],
        "North America": ["USA", "Canada"],
        "Europe": ["Spain", "France", "Germany", "Italy", "United Kingdom"],
    },
    "countries": ["Mexico", "USA", "Colombia", "Guatemala", "Honduras", "El Salvador",
                  "Costa Rica", "Panama", "Argentina", "Chile", "Peru", "Ecuador",
                  "Brazil", "Canada", "Spain", "France", "Germany", "Italy", "United Kingdom"]
}
with open(OUT / "territories.json", "w") as f:
    json.dump(territories, f, indent=2)

# ---------------------------------------------------------------------------
# 4. Albums / Tracks / Bridge (Screen 2 metadata + Screen 6 album analysis)
# ---------------------------------------------------------------------------
release_types = ["Album", "Compilation", "Greatest Hits", "Single", "Video Release"]
album_names = [
    "Pies Descalzos", "Donde Estan Los Ladrones", "Laundry Service", "Fijacion Oral Vol.1",
    "Sale el Sol", "El Dorado", "Grandes Exitos", "Loba (Deluxe)", "Vivir la Vida - Live",
    "Waka Waka - Single", "Hips Don't Lie - Single", "Te Felicito - Video Release",
    "Duele El Corazon - Single", "Antologia", "Sonora - Single"
]
albums = []
for i, name in enumerate(album_names, start=1):
    if "Grandes Exitos" in name or "Antologia" in name:
        rtype = "Greatest Hits"
    elif "Deluxe" in name and "Loba" in name:
        rtype = "Compilation"
    elif "Single" in name:
        rtype = "Single"
    elif "Video" in name:
        rtype = "Video Release"
    elif "Live" in name:
        rtype = "Compilation"
    else:
        rtype = "Album"
    year = random.choice([2001, 2002, 2005, 2009, 2010, 2011, 2014, 2016, 2019, 2020, 2022, 2023])
    track_count = random.randint(1, 16) if rtype != "Single" else 1
    albums.append({
        "album_id": f"ALB{i:03d}",
        "album_name": name,
        "release_type": rtype,
        "is_compilation": rtype in ["Compilation", "Greatest Hits"],
        "release_year": year,
        "track_count": track_count,
        "current_revenue_usd": round(random.uniform(15000, 950000), 2),
    })
with open(OUT / "albums.json", "w") as f:
    json.dump(albums, f, indent=2)

track_first_names = ["Hips Don't Lie", "Waka Waka", "Te Felicito", "Chantaje", "La Tortura",
                      "Ojos Asi", "Loba", "Rabiosa", "Antologia", "Suerte", "Underneath Your Clothes",
                      "Objection (Tango)", "Whenever, Wherever", "Empire", "Perro Fiel",
                      "Girl Like Me", "Don't Wait Up", "Me Enamore", "Nada", "Monotonia"]
tracks = []
for i, tname in enumerate(track_first_names, start=1):
    album = random.choice(albums)
    tracks.append({
        "track_id": f"TRK{i:03d}",
        "track_name": tname,
        "isrc": f"USRC1{1700000 + i}",
        "release_year": album["release_year"],
        "first_stream_date": f"{album['release_year']}-{random.randint(1,12):02d}-{random.randint(1,28):02d}",
        "content_type": random.choice(["Audio", "Audio", "Audio", "Video"]),
        "primary_album_id": album["album_id"],
    })
with open(OUT / "tracks.json", "w") as f:
    json.dump(tracks, f, indent=2)

bridge = []
for t in tracks:
    bridge.append({"track_id": t["track_id"], "album_id": t["primary_album_id"], "is_primary": True})
    # occasionally also appears on a compilation
    if random.random() < 0.3:
        comp = random.choice([a for a in albums if a["is_compilation"]])
        bridge.append({"track_id": t["track_id"], "album_id": comp["album_id"], "is_primary": False})
with open(OUT / "track_album_bridge.json", "w") as f:
    json.dump(bridge, f, indent=2)

# ---------------------------------------------------------------------------
# 5. Consumption & Revenue by release-year bucket (Screens 4 & 5)
# ---------------------------------------------------------------------------
buckets = ["Older than 10 years", "2017-2020", "2021", "2022", "2023", "2024", "2025"]
release_year_analysis = []
base = 42_000_000
for b in buckets:
    base = base * random.uniform(0.85, 1.35)
    consumption = round(base)
    revenue = round(consumption * random.uniform(0.0028, 0.0045), 2)
    yoy = round(random.uniform(-8, 34), 1)
    release_year_analysis.append({
        "bucket": b,
        "consumption_streams": consumption,
        "revenue_usd": revenue,
        "yoy_growth_pct": yoy,
    })
with open(OUT / "release_year_analysis.json", "w") as f:
    json.dump(release_year_analysis, f, indent=2)

# Catalog age split (older than 10y vs recent)
catalog_age_split = {
    "older_than_10y_pct": 75,
    "recent_releases_pct": 25,
}
with open(OUT / "catalog_age_split.json", "w") as f:
    json.dump(catalog_age_split, f, indent=2)

# Audio/Video x Premium/Ad-Supported consumption by release year (Screen 4 tabs)
consumption_matrix = []
for b in buckets:
    row_base = random.uniform(3_000_000, 14_000_000)
    consumption_matrix.append({
        "bucket": b,
        "audio_premium": round(row_base * 0.52),
        "audio_ad_supported": round(row_base * 0.28),
        "video_premium": round(row_base * 0.11),
        "video_ad_supported": round(row_base * 0.09),
    })
with open(OUT / "consumption_matrix.json", "w") as f:
    json.dump(consumption_matrix, f, indent=2)

# YoY growth trend (Screen 4 growth analysis)
growth_trend = [
    {"year": 2021, "yoy_growth_pct": 9.1},
    {"year": 2022, "yoy_growth_pct": 16.4},
    {"year": 2023, "yoy_growth_pct": 19.8},
    {"year": 2024, "yoy_growth_pct": 24.0},
    {"year": 2025, "yoy_growth_pct": 14.0},
]
with open(OUT / "growth_trend.json", "w") as f:
    json.dump(growth_trend, f, indent=2)

# Market growth comparison (Screen 4)
market_growth = {"artist_growth_pct": 34, "market_growth_pct": 14}
with open(OUT / "market_growth.json", "w") as f:
    json.dump(market_growth, f, indent=2)

# ---------------------------------------------------------------------------
# 6. PPD & Local/ROW revenue (Screen 5 / revenue conversion)
# ---------------------------------------------------------------------------
ppd = {
    "current_splits": {"Audio": 0.0041, "Video": 0.0019},
    "future_splits": {
        "Audio Premium": 0.0052, "Audio Ad Supported": 0.0011,
        "Video Premium": 0.0027, "Video Ad Supported": 0.0008,
        "Spotify": 0.0044, "Apple": 0.0071, "YouTube": 0.0018,
        "Amazon": 0.0052, "TikTok": 0.0006,
    }
}
with open(OUT / "ppd.json", "w") as f:
    json.dump(ppd, f, indent=2)

local_row = {
    "local_revenue_usd": 4_820_000,
    "row_revenue_usd": 11_940_000,
    "local_territories": ["Mexico", "USA", "Colombia"]
}
with open(OUT / "local_row_revenue.json", "w") as f:
    json.dump(local_row, f, indent=2)

# ---------------------------------------------------------------------------
# 7. New Release forecasting (Screen 7)
# ---------------------------------------------------------------------------
new_release_tracks = []
for i in range(1, 13):
    streams = round(random.uniform(0.6, 5.4), 2)
    new_release_tracks.append({
        "track_id": f"NR{i:03d}",
        "track_name": f"New Release Track {i}",
        "release_year": random.choice([2020, 2021, 2022, 2023, 2024]),
        "first_12m_streams_millions": streams,
        "months_of_data": random.choice([12, 12, 12, 6, 9]),
        "flag": random.choice([None, None, None, "Duplicate", "Collaboration", "Outlier", "Incomplete Data"]),
    })
with open(OUT / "new_release_tracks.json", "w") as f:
    json.dump(new_release_tracks, f, indent=2)

# ---------------------------------------------------------------------------
# 8. Corporate export summary (Screen 8)
# ---------------------------------------------------------------------------
corporate_export = {
    "catalog_name": "CHI Records",
    "local_territories": ["Mexico", "USA", "Colombia"],
    "total_tracks": 482,
    "total_albums": 41,
    "current_annual_revenue_usd": 16_760_000,
    "local_revenue_usd": 4_820_000,
    "row_revenue_usd": 11_940_000,
    "catalog_age_split": {"older_than_10y_pct": 75, "recent_pct": 25},
    "yoy_growth_pct_2025": 14.0,
    "market_growth_pct_2025": 14.0,
    "artist_vs_market_index_pct": 243,
    "expected_growth_pct": 8.0,
    "expected_decay_pct": -6.0,
    "average_new_track_streams_millions": 2.6,
    "projected_next_album_streams_millions": 26.0,
}
with open(OUT / "corporate_export.json", "w") as f:
    json.dump(corporate_export, f, indent=2)

print("Generated all JSON data files in", OUT)
