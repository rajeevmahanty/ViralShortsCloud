from app.services.viral_topic import get_viral_topic
from app.services.script_generator import generate_script


def main():
    topic = get_viral_topic()
    script = generate_script(topic["topic"])

    print("ViralShortsCloud pipeline started successfully.")
    print(f"Topic: {topic['topic']}")
    print(f"Source: {topic['source']}")
    print(f"Created: {topic['created_at']}")
    print()
    print("Generated Script:")
    print(f"Hook: {script['hook']}")
    print(f"Body: {script['body']}")
    print(f"Ending: {script['ending']}")


if __name__ == "__main__":
    main()