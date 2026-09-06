import json
import os
import tempfile

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

VIDEO_FILE = os.path.join(
    BASE_DIR,
    "output",
    "ViralShortsCloud_Final.mp4"
)

METADATA_FILE = os.path.join(
    BASE_DIR,
    "output",
    "youtube_metadata.json"
)

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload"
]


def get_credentials():

    token_json = os.environ.get("YOUTUBE_TOKEN_JSON")

    if not token_json:
        raise RuntimeError(
            "YOUTUBE_TOKEN_JSON GitHub Secret is missing."
        )

    temp_file = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".json",
            delete=False,
            encoding="utf-8"
        ) as file:

            file.write(token_json)
            temp_file = file.name

        credentials = Credentials.from_authorized_user_file(
            temp_file,
            SCOPES
        )

    finally:

        if temp_file and os.path.exists(temp_file):
            os.remove(temp_file)

    if credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())

    if not credentials.valid:
        raise RuntimeError(
            "YouTube OAuth token is invalid or expired."
        )

    return credentials


def upload_video():

    if not os.path.exists(VIDEO_FILE):
        raise FileNotFoundError(
            f"Video not found: {VIDEO_FILE}"
        )

    if not os.path.exists(METADATA_FILE):
        raise FileNotFoundError(
            f"Metadata not found: {METADATA_FILE}"
        )

    credentials = get_credentials()

    youtube = build(
        "youtube",
        "v3",
        credentials=credentials
    )

    with open(
        METADATA_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        metadata = json.load(file)

    body = {
        "snippet": {
            "title": metadata["title"],
            "description": metadata["description"],
            "tags": metadata["tags"],
            "categoryId": "27"
        },

        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False
        }
    }

    media = MediaFileUpload(
        VIDEO_FILE,
        mimetype="video/mp4",
        resumable=True
    )

    print("\n========================================")
    print("       YOUTUBE PUBLIC UPLOAD")
    print("========================================")

    print("Title:", body["snippet"]["title"])
    print("Privacy:", body["status"]["privacyStatus"])

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )

    response = None

    while response is None:

        status, response = request.next_chunk()

        if status:
            print(
                f"Upload progress: "
                f"{int(status.progress() * 100)}%"
            )

    video_id = response.get("id")

    if not video_id:
        raise RuntimeError(
            f"YouTube returned no video ID: {response}"
        )

    print("\n========================================")
    print("       PUBLIC UPLOAD SUCCESS")
    print("========================================")

    print("Video ID:", video_id)
    print(
        "Shorts:",
        f"https://youtube.com/shorts/{video_id}"
    )

    print("\nVIDEO IS PUBLIC.")
    print("========================================")


if __name__ == "__main__":
    upload_video()
