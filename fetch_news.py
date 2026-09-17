import feedparser
import json
import re
from datetime import datetime, timezone
from html import unescape


# --------------------------------------------------
# Einstellungen
# --------------------------------------------------

FEEDS = [
    {
        "category": "gaming",
        "name": "PC Gamer",
        "url": "https://www.pcgamer.com/rss/",
        "base_score": 3
    },

    {
        "category": "nfl",
        "name": "Minnesota Vikings",
        "url": "https://www.vikings.com/rss/news",
        "base_score": 8
    },

    {
        "category": "pharma",
        "name": "Fierce Pharma",
        "url": "https://www.fiercepharma.com/rss/xml",
        "base_score": 4
    }
]


# --------------------------------------------------
# Persönliche Interessen
# Begriff : Zusatzpunkte
# --------------------------------------------------

KEYWORDS = {

    "gaming": {
        "world of warcraft": 8,
        "wow": 5,
        "diablo": 7,
        "blizzard": 6,
        "warhammer": 6,
        "nvidia": 4,
        "amd": 4,
        "steam": 3,
        "pc gaming": 3
    },

    "nfl": {
        "minnesota vikings": 15,
        "vikings": 10,
        "nfl draft": 6,
        "playoffs": 5,
        "super bowl": 5,
        "trade": 4,
        "injury": 4,
        "roster": 4
    },

    "pharma": {
        "novartis": 15,
        "kymriah": 20,
        "car-t": 15,
        "car t": 15,
        "cell therapy": 10,
        "fda": 5,
        "ema": 5,
        "phase iii": 6,
        "clinical trial": 4
    }
}


# --------------------------------------------------
# Hilfsfunktionen
# --------------------------------------------------

def clean_html(text):

    if not text:
        return ""

    text = re.sub(r"<[^>]+>", " ", text)
    text = unescape(text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def calculate_score(category, title, description, base_score):

    score = base_score

    text = (
        title + " " + description
    ).lower()

    category_keywords = KEYWORDS.get(category, {})

    for keyword, points in category_keywords.items():

        if keyword.lower() in text:
            score += points

    return score


# --------------------------------------------------
# News abrufen
# --------------------------------------------------

print("📰 MY NEWS – News-Abruf gestartet")

articles = []


for feed_info in FEEDS:

    print("")
    print(f"📡 Lade {feed_info['name']}...")

    feed = feedparser.parse(feed_info["url"])

    print(
        f"   {len(feed.entries)} Meldungen gefunden"
    )


    for entry in feed.entries[:25]:

        title = clean_html(
            entry.get("title", "")
        )

        description = clean_html(
            entry.get("summary", "")
        )

        url = entry.get(
            "link",
            "#"
        )


        score = calculate_score(
            feed_info["category"],
            title,
            description,
            feed_info["base_score"]
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

            "score":
                score
        }


        articles.append(article)


# --------------------------------------------------
# Duplikate entfernen
# --------------------------------------------------

unique_articles = []

seen_urls = set()


for article in articles:

    url = article["url"]

    if url in seen_urls:
        continue

    seen_urls.add(url)

    unique_articles.append(article)


# --------------------------------------------------
# Nach Relevanz sortieren
# --------------------------------------------------

unique_articles.sort(
    key=lambda article: article["score"],
    reverse=True
)


# --------------------------------------------------
# JSON erstellen
# --------------------------------------------------

news = {

    "updated":
        datetime.now(
            timezone.utc
        ).isoformat(),

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


print("")
print(
    f"✅ {len(unique_articles)} Meldungen gespeichert"
)

print("⭐ Höchste Relevanz:")

for article in unique_articles[:5]:

    print(
        article["score"],
        "-",
        article["title"]
    )

print("")
print("✅ news.json aktualisiert")
