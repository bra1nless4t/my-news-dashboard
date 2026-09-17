import feedparser
import json
import re
from datetime import datetime, timezone
from html import unescape
from email.utils import parsedate_to_datetime


FEEDS = [

    # ==========================================
    # WARHAMMER 40K
    # ==========================================

    {
        "category": "warhammer",
        "name": "Goonhammer",
        "url": "https://www.goonhammer.com/feed/",
        "base_score": 5,
        "filter_40k": True
    },

    {
        "category": "warhammer",
        "name": "Bell of Lost Souls",
        "url": "https://feeds2.feedburner.com/BellOfLostSouls",
        "base_score": 4,
        "filter_40k": True
    },


    # ==========================================
    # GAMING
    # ==========================================

    {
        "category": "gaming",
        "name": "PC Gamer",
        "url": "https://www.pcgamer.com/rss/",
        "base_score": 4
    },

    {
        "category": "gaming",
        "name": "GameStar",
        "url": "https://www.gamestar.de/rss/gaming.rss",
        "base_score": 4
    },


    # ==========================================
    # NFL
    # ==========================================

    {
        "category": "nfl",
        "name": "Minnesota Vikings",
        "url": "https://www.vikings.com/rss/news",
        "base_score": 8
    },

    {
        "category": "nfl",
        "name": "RTL NFL",
        "url": "https://www.rtl.de/rss/feed/sport/nfl/",
        "base_score": 3
    },


    # ==========================================
    # PHARMA
    # ==========================================

    {
        "category": "pharma",
        "name": "Fierce Pharma",
        "url": "https://www.fiercepharma.com/rss/xml",
        "base_score": 4
    }

]


# ==================================================
# PERSÖNLICHE INTERESSEN
# ==================================================

KEYWORDS = {

    "warhammer": {

        "world eaters": 15,
        "chaos space marines": 15,
        "chaos daemons": 12,
        "khorne": 10,
        "angron": 12,

        "warhammer 40,000": 8,
        "warhammer 40000": 8,
        "40k": 8,

        "space marines": 6,

        "balance dataslate": 12,
        "munitorum field manual": 12,
        "points": 7,

        "codex": 7,
        "errata": 8,
        "faq": 6,

        "11th edition": 12
    },


    "gaming": {

        "world of warcraft": 10,
        "wow": 6,

        "diablo": 8,
        "blizzard": 6,

        "warhammer": 7,

        "steam": 3,

        "nvidia": 5,
        "geforce": 5,

        "amd": 4,
        "radeon": 4,

        "playstation": 3,
        "xbox": 3,
        "nintendo": 3
    },


    "nfl": {

        "minnesota vikings": 15,
        "vikings": 10,

        "nfl draft": 7,

        "playoffs": 6,
        "super bowl": 5,

        "trade": 5,
        "roster": 5,

        "injury": 5,
        "injured": 5,

        "quarterback": 3
    },


    "pharma": {

        "novartis": 18,

        "kymriah": 25,

        "car-t": 18,
        "car t": 18,

        "cell therapy": 12,

        "fda": 6,
        "ema": 6,

        "phase iii": 7,
        "phase 3": 7,

        "clinical trial": 5,

        "approval": 5
    }
}


# ==================================================
# 40K FILTER
# ==================================================

WARHAMMER_40K_TERMS = [

    "40k",
    "warhammer 40,000",
    "warhammer 40000",

    "space marine",
    "space marines",

    "chaos space marine",
    "chaos space marines",

    "world eaters",
    "angron",
    "khorne",

    "chaos daemons",

    "tyranid",
    "orks",
    "aeldari",
    "drukhari",
    "necron",
    "tau",
    "t'au",

    "adeptus",
    "imperial guard",
    "astra militarum",

    "sisters of battle",
    "adepta sororitas",

    "genestealer",

    "custodes",

    "death guard",
    "thousand sons",

    "grey knights",

    "codex",

    "dataslate",
    "munitorum"
]


# ==================================================
# HTML BEREINIGEN
# ==================================================

def clean_html(text):

    if not text:
        return ""

    text = re.sub(
        r"<[^>]+>",
        " ",
        text
    )

    text = unescape(text)

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ==================================================
# DATUM AUS RSS LESEN
# ==================================================

def get_date(entry):

    date_fields = [
        "published",
        "updated",
        "created"
    ]

    for field in date_fields:

        value = entry.get(field)

        if not value:
            continue

        try:

            date = parsedate_to_datetime(value)

            if date.tzinfo is None:
                date = date.replace(
                    tzinfo=timezone.utc
                )

            return date.astimezone(
                timezone.utc
            )

        except Exception:
            pass


    return datetime.now(
        timezone.utc
    )


# ==================================================
# ALTER DES ARTIKELS
# ==================================================

def get_age_hours(date):

    now = datetime.now(
        timezone.utc
    )

    difference = now - date

    return max(
        0,
        difference.total_seconds() / 3600
    )


# ==================================================
# AKTUALITÄTSBONUS
# ==================================================

def freshness_score(age_hours):

    if age_hours <= 6:
        return 12

    if age_hours <= 12:
        return 10

    if age_hours <= 24:
        return 8

    if age_hours <= 48:
        return 5

    if age_hours <= 72:
        return 3

    if age_hours <= 168:
        return 1

    return 0


# ==================================================
# RELEVANZ BERECHNEN
# ==================================================

def calculate_score(
    category,
    title,
    description,
    base_score,
    age_hours
):

    score = base_score

    text = (
        title + " " + description
    ).lower()


    # Persönliche Interessen

    category_keywords = KEYWORDS.get(
        category,
        {}
    )

    for keyword, points in category_keywords.items():

        if keyword.lower() in text:

            score += points


    # Aktualität

    score += freshness_score(
        age_hours
    )


    return score


# ==================================================
# IST ES WARHAMMER 40K?
# ==================================================

def is_40k(title, description):

    text = (
        title + " " + description
    ).lower()

    return any(
        term in text
        for term in WARHAMMER_40K_TERMS
    )


# ==================================================
# NEWS ABRUFEN
# ==================================================

print("")
print("================================")
print("📰 MY NEWS")
print("================================")
print("")


articles = []


for feed_info in FEEDS:

    print(
        f"📡 Lade {feed_info['name']}..."
    )


    feed = feedparser.parse(
        feed_info["url"]
    )


    print(
        f"   → {len(feed.entries)} Meldungen gefunden"
    )


    added = 0


    for entry in feed.entries[:40]:

        title = clean_html(
            entry.get(
                "title",
                ""
            )
        )


        description = clean_html(
            entry.get(
                "summary",
                entry.get(
                    "description",
                    ""
                )
            )
        )


        # --------------------------
        # Warhammer 40K Filter
        # --------------------------

        if feed_info.get(
            "filter_40k",
            False
        ):

            if not is_40k(
                title,
                description
            ):

                continue


        url = entry.get(
            "link",
            "#"
        )


        publish_date = get_date(
            entry
        )


        age_hours = get_age_hours(
            publish_date
        )


        score = calculate_score(

            feed_info["category"],

            title,

            description,

            feed_info["base_score"],

            age_hours
        )


        article = {

            "category":
                feed_info["category"],

            "title":
                title,

            "description":
                description[:500],

            "source":
                feed_info["name"],

            "url":
                url,

            "published":
                publish_date.isoformat(),

            "age_hours":
                round(
                    age_hours,
                    1
                ),

            "score":
                score
        }


        articles.append(
            article
        )

        added += 1


    print(
        f"   → {added} relevante Meldungen übernommen"
    )

    print("")


# ==================================================
# DUPLIKATE ENTFERNEN
# ==================================================

unique_articles = []

seen_urls = set()
seen_titles = set()


for article in articles:

    url = article["url"]

    title_key = (
        article["title"]
        .lower()
        .strip()
    )


    if url in seen_urls:
        continue


    if title_key in seen_titles:
        continue


    seen_urls.add(
        url
    )

    seen_titles.add(
        title_key
    )

    unique_articles.append(
        article
    )


# ==================================================
# SORTIEREN
# ==================================================

unique_articles.sort(

    key=lambda article: (
        article["score"],
        article["published"]
    ),

    reverse=True
)


# ==================================================
# STATISTIK
# ==================================================

stats = {

    "warhammer": 0,
    "gaming": 0,
    "nfl": 0,
    "pharma": 0
}


for article in unique_articles:

    category = article["category"]

    if category in stats:

        stats[category] += 1


# ==================================================
# JSON
# ==================================================

news = {

    "updated":
        datetime.now(
            timezone.utc
        ).isoformat(),

    "stats":
        stats,

    "articles":
        unique_articles
}


with open(

    "news.json",

    "w",

    encoding="utf-8"

) as file:

    json.dump(

        news,

        file,

        ensure_ascii=False,

        indent=2
    )


# ==================================================
# LOG
# ==================================================

print("")
print("================================")
print("📊 STATISTIK")
print("================================")

print(
    f"⚔️ Warhammer: {stats['warhammer']}"
)

print(
    f"🎮 Gaming: {stats['gaming']}"
)

print(
    f"🏈 NFL: {stats['nfl']}"
)

print(
    f"🧬 Pharma: {stats['pharma']}"
)

print("")
print(
    f"✅ Insgesamt: {len(unique_articles)} Meldungen"
)


print("")
print("🔥 TOP NEWS")
print("--------------------------------")


for article in unique_articles[:10]:

    print(
        f"{article['score']:>3} Punkte | "
        f"{article['category']:<10} | "
        f"{article['title']}"
    )


print("")
print("✅ news.json aktualisiert")
