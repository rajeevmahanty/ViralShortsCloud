from app.services.viral_topic import get_viral_topic


def main():
    topic = get_viral_topic()
    print("ViralShortsCloud pipeline started successfully.")
    print(f"Topic: {topic['topic']}")
    print(f"Source: {topic['source']}")
    print(f"Created: {topic['created_at']}")


if __name__ == "__main__":
    main()
