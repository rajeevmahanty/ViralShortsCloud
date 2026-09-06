from datetime import datetime


def get_viral_topic():
    return {
        "topic": "5 surprising facts about the human brain",
        "source": "local_seed",
        "created_at": datetime.utcnow().isoformat()
    }


if __name__ == "__main__":
    print(get_viral_topic())
