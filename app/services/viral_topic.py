from datetime import datetime
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET


TOPICS = [
    "5 surprising facts about the human brain",
    "5 unbelievable facts about space",
    "5 strange facts about the ocean",
    "5 amazing facts about animals",
    "5 mysteries scientists still cannot explain",
    "5 incredible facts about the human body",
    "5 places on Earth that look unreal",
    "5 historical facts you probably never learned"
]

TRENDS_URL = "https://trends.google.com/trending/rss?geo=US"

BLOCKED_WORDS = [
    "schedule",
    "match",
    "matches",
    "score",
    "scores",
    "live",
    "fixture",
    "fixtures",
    "odds",
    "betting",
    "weather",
    "temperature",
    "stock",
    "stocks",
    "price",
    "prices",
    "coupon",
    "sale",
    "lottery"
]


def is_good_topic(title):
    lowered = title.lower()

    if len(title) < 5 or len(title) > 80:
        return False

    for word in BLOCKED_WORDS:
        if word in lowered:
            return False

    return True


def get_trending_topic():
    request = Request(
        TRENDS_URL,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    with urlopen(request, timeout=10) as response:
        data = response.read()

    root = ET.fromstring(data)

    for item in root.findall(".//item"):
        title = item.findtext("title")

        if title:
            title = " ".join(title.strip().split())

            if is_good_topic(title):
                return {
                    "topic": f"5 surprising facts about {title}",
                    "source": "google_trends_rss",
                    "created_at": datetime.utcnow().isoformat()
                }

    raise RuntimeError("No suitable trending topic found")


def get_viral_topic():
    try:
        return get_trending_topic()
    except Exception as error:
        index = datetime.utcnow().day % len(TOPICS)

        return {
            "topic": TOPICS[index],
            "source": "topic_pool_fallback",
            "created_at": datetime.utcnow().isoformat(),
            "error": str(error)
        }


if __name__ == "__main__":
    print(get_viral_topic())
