from urllib.parse import quote
from urllib.request import Request, urlopen
import json
import re


WIKIPEDIA_API = "https://en.wikipedia.org/w/api.php"


def wikipedia_request(params):
    query = "&".join(
        f"{quote(str(key))}={quote(str(value))}"
        for key, value in params.items()
    )
    request = Request(
        f"{WIKIPEDIA_API}?{query}",
        headers={"User-Agent": "ViralShortsCloud/1.0"}
    )
    with urlopen(request, timeout=15) as response:
        return json.loads(response.read().decode("utf-8"))


def search_wikipedia(topic):
    data = wikipedia_request({
        "action": "query",
        "list": "search",
        "srsearch": topic,
        "format": "json",
        "utf8": "1",
        "srlimit": "5"
    })

    results = data.get("query", {}).get("search", [])

    if not results:
        raise RuntimeError(f"No Wikipedia article found for: {topic}")

    return [result["title"] for result in results]


def get_wikipedia_summary(title):
    data = wikipedia_request({
        "action": "query",
        "prop": "extracts",
        "exintro": "1",
        "explaintext": "1",
        "titles": title,
        "format": "json",
        "formatversion": "2"
    })

    pages = data.get("query", {}).get("pages", [])

    if not pages:
        raise RuntimeError(f"No Wikipedia content found for: {title}")

    extract = pages[0].get("extract", "").strip()

    if not extract:
        raise RuntimeError(f"No usable Wikipedia summary for: {title}")

    return extract


def extract_facts(text):
    text = re.sub(r"\s+", " ", text).strip()

    sentences = re.split(r"(?<=[.!?])\s+", text)

    facts = []

    for sentence in sentences:
        sentence = sentence.strip()

        if len(sentence) < 45 or len(sentence) > 280:
            continue

        lowered = sentence.lower()

        blocked = [
            "may be",
            "might be",
            "could be",
            "citation needed",
            "disambiguation"
        ]

        if any(word in lowered for word in blocked):
            continue

        if sentence not in facts:
            facts.append(sentence)

        if len(facts) == 5:
            break

    return facts


def make_spoken_fact(sentence):
    sentence = sentence.strip()
    sentence = re.sub(r"\([^)]*\)", "", sentence)
    sentence = sentence.replace('"', "")
    sentence = re.sub(r"\s+", " ", sentence).strip()
    return sentence


def generate_script(topic):
    clean_topic = topic.strip()

    if not clean_topic:
        raise ValueError("Topic cannot be empty")

    titles = search_wikipedia(clean_topic)

    last_error = None

    for wikipedia_title in titles:

        try:
            summary = get_wikipedia_summary(wikipedia_title)

            facts = extract_facts(summary)

            if len(facts) < 5:
                last_error = (
                    f"{wikipedia_title}: only {len(facts)} usable facts"
                )
                continue

            spoken_facts = [
                make_spoken_fact(fact)
                for fact in facts
            ]

            return {
                "topic": clean_topic,
                "source": "Wikipedia",
                "source_title": wikipedia_title,
                "hook": (
                    f"Stop scrolling! Here are 5 fascinating facts "
                    f"about {clean_topic}."
                ),
                "fact_1": spoken_facts[0],
                "fact_2": spoken_facts[1],
                "fact_3": spoken_facts[2],
                "fact_4": spoken_facts[3],
                "fact_5": spoken_facts[4],
                "ending": (
                    "Which fact surprised you the most? "
                    "Follow for more!"
                )
            }

        except Exception as error:
            last_error = str(error)

    raise RuntimeError(
        f"Could not find 5 usable researched facts for "
        f"'{clean_topic}'. Last error: {last_error}"
    )


if __name__ == "__main__":
    result = generate_script("Tribeca")

    print("===== SHORTS SCRIPT =====")
    print(f"Topic: {result['topic']}")
    print(f"Source: {result['source']}")
    print(f"Article: {result['source_title']}")
    print()
    print(result["hook"])
    print()
    print("1.", result["fact_1"])
    print("2.", result["fact_2"])
    print("3.", result["fact_3"])
    print("4.", result["fact_4"])
    print("5.", result["fact_5"])
    print()
    print(result["ending"])
