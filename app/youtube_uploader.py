import json
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


TOKEN_FILE = r"C:\Users\rajee\token.json"

VIDEO_FILE = (
    r"C:\Users\rajee\ViralShortsCloud"
    r"\output\ViralShortsCloud_Final.mp4"
)

METADATA_FILE = (
    r"C:\Users\rajee\ViralShortsCloud"
    r"\output\youtube_metadata.json"
)

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload"
]


def upload_video():

    if not os.path.exists(TOKEN_FILE):
        raise FileNotFoundError(
            f"YouTube token not found: {TOKEN_FILE}"
        )

    if not os.path.exists(VIDEO_FILE):
        raise FileNotFoundError(
            f"Video not found: {VIDEO_FILE}"
        )

    if not os.path.exists(METADATA_FILE):
        raise FileNotFoundError(
            f"Metadata not found: {METADATA_FILE}"
        )

    # --------------------------------------------------------
    # LOAD EXISTING YOUTUBE AUTH
    # --------------------------------------------------------

    credentials = Credentials.from_authorized_user_file(
        TOKEN_FILE,
        SCOPES
    )

    if credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())

    if not credentials.valid:
        raise RuntimeError(
            "YouTube OAuth token is invalid."
        )

    youtube = build(
        "youtube",
        "v3",
        credentials=credentials
    )

    # --------------------------------------------------------
    # LOAD GENERATED METADATA
    # --------------------------------------------------------

    with open(
        METADATA_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        metadata = json.load(file)

    # --------------------------------------------------------
    # FORCE PUBLIC
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # UPLOAD
    # --------------------------------------------------------

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
    print(
        "File size:",
        round(os.path.getsize(VIDEO_FILE) / 1024 / 1024, 2),
        "MB"
    )

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
        "YouTube:",
        f"https://www.youtube.com/watch?v={video_id}"
    )
    print(
        "Shorts:",
        f"https://youtube.com/shorts/{video_id}"
    )

    print("\nVIDEO IS PUBLIC.")
    print("========================================")


if __name__ == "__main__":
    upload_video()
