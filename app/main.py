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
    print("Generated Short Script:")
    print(f"Hook: {script['hook']}")
    print(f"Fact 1: {script['fact_1']}")
    print(f"Fact 2: {script['fact_2']}")
    print(f"Fact 3: {script['fact_3']}")
    print(f"Fact 4: {script['fact_4']}")
    print(f"Fact 5: {script['fact_5']}")
    print(f"Ending: {script['ending']}")


if __name__ == "__main__":
    main()
