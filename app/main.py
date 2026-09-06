from app.services.viral_topic import get_viral_topic
from app.services.script_generator import generate_script


def main():
    topic = get_viral_topic()

    print("ViralShortsCloud pipeline started successfully.")
    print(f"Topic: {topic['topic']}")
    print(f"Source: {topic['source']}")
    print(f"Created: {topic['created_at']}")
    print()

    try:
        script = generate_script(topic["topic"])

        print("===== RESEARCHED SHORT SCRIPT =====")
        print(f"Research Source: {script['source']}")
        print(f"Wikipedia Article: {script['source_title']}")
        print()
        print(f"Hook: {script['hook']}")
        print(f"Fact 1: {script['fact_1']}")
        print(f"Fact 2: {script['fact_2']}")
        print(f"Fact 3: {script['fact_3']}")
        print(f"Fact 4: {script['fact_4']}")
        print(f"Fact 5: {script['fact_5']}")
        print(f"Ending: {script['ending']}")

    except Exception as error:
        print()
        print("SCRIPT GENERATION FAILED")
        print(f"Reason: {error}")
        raise


if __name__ == "__main__":
    main()
