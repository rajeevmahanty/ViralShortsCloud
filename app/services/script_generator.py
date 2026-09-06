def generate_script(topic):
    clean_topic = topic.strip()

    return {
        "hook": f"Stop scrolling! Here are 5 unbelievable facts about {clean_topic}.",
        "fact_1": f"First, {clean_topic} is far more surprising than most people realize.",
        "fact_2": "Second, scientists have discovered details about this topic that challenge what we normally expect.",
        "fact_3": "Third, one of the most interesting facts is something most people never hear about.",
        "fact_4": "Fourth, the deeper you look, the stranger and more fascinating this subject becomes.",
        "fact_5": "And finally, the last fact might completely change the way you think about it.",
        "ending": "Which fact surprised you the most? Follow for more amazing facts!"
    }


if __name__ == "__main__":
    result = generate_script("places on Earth that look unreal")

    print("===== GENERATED SHORT SCRIPT =====")
    print(f"Hook: {result['hook']}")
    print(f"Fact 1: {result['fact_1']}")
    print(f"Fact 2: {result['fact_2']}")
    print(f"Fact 3: {result['fact_3']}")
    print(f"Fact 4: {result['fact_4']}")
    print(f"Fact 5: {result['fact_5']}")
    print(f"Ending: {result['ending']}")
