import feedparser
import json
from datetime import datetime, timezone

print("📰 MY NEWS – News-Abruf gestartet")

FEEDS = [
    {
        "category": "gaming",
        "name": "PC Gamer",
        "url": "https://www.pcgamer.com/rss/"
    }
]

articles = []

for feed_info in FEEDS:

    print(f"📡 Lade {feed_info['name']}...")

    feed = feedparser.parse(feed_info["url"])

    print(f"   {len(feed.entries)} Meldungen gefunden")

    for entry in feed.entries[:15]:

        article = {
            "category": feed_info["category"],
            "title": entry.get("title", "Keine Überschrift"),
            "description": entry.get("summary", ""),
            "source": feed_info["name"],
            "url": entry.get("link", "#"),
            "score": 5
        }

        articles.append(article)


news = {
    "updated": datetime.now(timezone.utc).isoformat(),
    "articles": articles
}


with open("news.json", "w", encoding="utf-8") as file:

    json.dump(
        news,
        file,
        ensure_ascii=False,
        indent=2
    )


print("")
print(f"✅ {len(articles)} echte Meldungen gespeichert")
print("✅ news.json wurde aktualisiert")
