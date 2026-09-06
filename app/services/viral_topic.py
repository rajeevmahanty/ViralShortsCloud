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
            title = title.strip()

            if len(title) >= 3:
                return {
                    "topic": f"5 surprising facts about {title}",
                    "source": "google_trends_rss",
                    "created_at": datetime.utcnow().isoformat()
                }

    raise RuntimeError("No trending topics found")


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
