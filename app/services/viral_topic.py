from datetime import datetime


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


def get_viral_topic():
    index = datetime.utcnow().day % len(TOPICS)

    return {
        "topic": TOPICS[index],
        "source": "topic_pool",
        "created_at": datetime.utcnow().isoformat()
    }


if __name__ == "__main__":
    print(get_viral_topic())
