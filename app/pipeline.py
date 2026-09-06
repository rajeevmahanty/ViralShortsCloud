import json
import os
import re
import subprocess
import sys
from datetime import datetime

from services.viral_topic import get_viral_topic
from services.script_generator import generate_script


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

SCRIPT_FILE = os.path.join(OUTPUT_DIR, "narration.txt")
AUDIO_FILE = os.path.join(OUTPUT_DIR, "narration.wav")
VIDEO_FILE = os.path.join(OUTPUT_DIR, "ViralShortsCloud_Final.mp4")
METADATA_FILE = os.path.join(OUTPUT_DIR, "youtube_metadata.json")


def run_command(command):
    print("\n$", " ".join(command))
    subprocess.run(command, check=True)


def clean_filename(value):
    value = re.sub(r"[^A-Za-z0-9_-]+", "_", value)
    return value.strip("_")[:60] or "viral_short"


def build_narration(script):
    return "\n\n".join([
        script["hook"],
        script["fact_1"],
        script["fact_2"],
        script["fact_3"],
        script["fact_4"],
        script["fact_5"],
        script["ending"],
    ])


def main():

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("\n===== STEP 1: TRENDING TOPIC =====")

    trend = get_viral_topic()
    topic = trend["topic"]

    print("Topic:", topic)
    print("Trend source:", trend.get("source"))

    print("\n===== STEP 2: RESEARCH + SCRIPT =====")

    script = generate_script(topic)

    print("Research source:", script["source"])
    print("Article:", script["source_title"])

    narration = build_narration(script)

    with open(SCRIPT_FILE, "w", encoding="utf-8") as file:
        file.write(narration)

    print("\n===== STEP 3: AI NARRATION =====")

    if os.name == "nt":
        model = r"C:\Users\rajee\en_US-lessac-medium.onnx"

        if not os.path.exists(model):
            raise FileNotFoundError(
                f"Local Piper model not found: {model}"
            )

        piper_command = [
            "piper",
            "-m",
            model,
            "-f",
            AUDIO_FILE,
            "-i",
            SCRIPT_FILE,
            "--sentence-silence",
            "0.15",
        ]

    else:
        piper_command = [
            "piper",
            "--model",
            "en_US-lessac-medium",
            "--output_file",
            AUDIO_FILE,
            "--input_file",
            SCRIPT_FILE,
            "--sentence-silence",
            "0.15",
        ]

    run_command(piper_command)

    print("\n===== STEP 4: CREATE SHORT =====")

    filter_complex = (
        "[0:v]"
        "scale=1080:1920:force_original_aspect_ratio=increase,"
        "crop=1080:1920,"
        "drawbox=x=18:y=18:w=1044:h=1884:"
        "color=0x1683FF@0.95:t=8,"
        "drawbox=x=55:y=360:w=970:h=1180:"
        "color=black@0.38:t=fill,"
        "format=yuv420p"
        "[v]"
    )

    run_command([
        "ffmpeg",
        "-y",
        "-f", "lavfi",
        "-i", "color=c=0x07111f:s=1080x1920:r=30",
        "-i", AUDIO_FILE,
        "-filter_complex", filter_complex,
        "-map", "[v]",
        "-map", "1:a",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "24",
        "-c:a", "aac",
        "-b:a", "128k",
        "-shortest",
        VIDEO_FILE,
    ])

    print("\n===== STEP 5: YOUTUBE METADATA =====")

    short_title = topic.strip()

    if len(short_title) > 85:
        short_title = short_title[:82] + "..."

    metadata = {
        "title": f"{short_title} #Shorts",

        "description": (
            f"Discover fascinating facts about {topic}.\n\n"
            "Created automatically by ViralShortsCloud.\n\n"
            "#Shorts #Facts #DidYouKnow"
        ),

        "tags": [
            "shorts",
            "facts",
            "did you know",
            "interesting facts",
            clean_filename(topic).replace("_", " ")
        ],

        "privacyStatus": "public",
        "topic": topic,
        "source": script["source"],
        "source_title": script["source_title"],
        "generated_at": datetime.utcnow().isoformat(),
    }

    with open(METADATA_FILE, "w", encoding="utf-8") as file:
        json.dump(
            metadata,
            file,
            indent=2,
            ensure_ascii=False
        )

    print(json.dumps(
        metadata,
        indent=2,
        ensure_ascii=False
    ))

    print("\n===== VIDEO GENERATION COMPLETE =====")
    print("Video:", VIDEO_FILE)
    print("Metadata:", METADATA_FILE)

    return 0


if __name__ == "__main__":
    sys.exit(main())
