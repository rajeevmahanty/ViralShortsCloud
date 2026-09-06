def generate_script(topic):
    return {
        "hook": f"You won't believe these facts about {topic}!",
        "body": f"Today we're exploring {topic}. Stay until the end for the most surprising one.",
        "ending": "Which one surprised you the most? Follow for more!"
    }


if __name__ == "__main__":
    result = generate_script("5 places on Earth that look unreal")
    print(result)