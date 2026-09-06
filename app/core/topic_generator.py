from datetime import datetime


def generate_topic():
    return {
        "topic": "5 surprising facts about the human brain",
        "created_at": datetime.utcnow().isoformat()
    }


if __name__ == "__main__":
    print(generate_topic())
