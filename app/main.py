from app.core.topic_generator import generate_topic


def main():
    topic = generate_topic()
    print("ViralShortsCloud pipeline started successfully.")
    print(f"Topic: {topic['topic']}")
    print(f"Created: {topic['created_at']}")


if __name__ == "__main__":
    main()
