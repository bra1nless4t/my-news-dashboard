import json
from datetime import datetime, timezone

print("📰 MY NEWS – News-Abruf gestartet")

news = {
    "updated": datetime.now(timezone.utc).isoformat(),
    "articles": [
        {
            "category": "warhammer",
            "title": "Warhammer 40K Testmeldung",
            "description": "Der automatische News-Abruf funktioniert.",
            "source": "MY NEWS",
            "url": "#",
            "score": 10
        },
        {
            "category": "gaming",
            "title": "Gaming Testmeldung",
            "description": "Hier erscheinen später aktuelle Gaming-News.",
            "source": "MY NEWS",
            "url": "#",
            "score": 8
        },
        {
            "category": "nfl",
            "title": "Minnesota Vikings Testmeldung",
            "description": "Hier erscheinen später aktuelle Vikings- und NFL-News.",
            "source": "MY NEWS",
            "url": "#",
            "score": 10
        },
        {
            "category": "pharma",
            "title": "Novartis / Pharma Testmeldung",
            "description": "Hier erscheinen später aktuelle Pharma-News.",
            "source": "MY NEWS",
            "url": "#",
            "score": 10
        }
    ]
}

with open("news.json", "w", encoding="utf-8") as file:
    json.dump(news, file, ensure_ascii=False, indent=2)

print(f"✅ {len(news['articles'])} Meldungen gespeichert")
print("✅ news.json wurde erstellt")
