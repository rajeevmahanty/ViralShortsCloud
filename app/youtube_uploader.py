import json
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


TOKEN_FILE = r"C:\Users\rajee\token.json"
VIDEO_FILE = r"C:\Users\rajee\ViralShortsCloud\output\ViralShortsCloud_Final.mp4"
METADATA_FILE = r"C:\Users\rajee\ViralShortsCloud\output\youtube_metadata.json"

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]


def upload_video():
    if not os.path.exists(TOKEN_FILE):
        raise FileNotFoundError(TOKEN_FILE)

    if not os.path.exists(VIDEO_FILE):
        raise FileNotFoundError(VIDEO_FILE)

    if not os.path.exists(METADATA_FILE):
        raise FileNotFoundError(METADATA_FILE)

    credentials = Credentials.from_authorized_user_file(
        TOKEN_FILE,
        SCOPES
    )

    if credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())

    if not credentials.valid:
        raise RuntimeError("YouTube OAuth token is invalid.")

    with open(METADATA_FILE, "r", encoding="utf-8") as file:
        metadata = json.load(file)

    youtube = build(
        "youtube",
        "v3",
        credentials=credentials
    )

    body = {
        "snippet": {
            "title": metadata["title"],
            "description": metadata["description"],
            "tags": metadata["tags"],
            "categoryId": "27"
        },
        "status": {
            "privacyStatus": metadata.get("privacyStatus", "private"),
            "selfDeclaredMadeForKids": False
        }
    }

    media = MediaFileUpload(
        VIDEO_FILE,
        mimetype="video/mp4",
        resumable=True
    )

    print("\n===== YOUTUBE UPLOAD =====")
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
                f"Upload progress: {int(status.progress() * 100)}%"
            )

    video_id = response["id"]

    print("\n===== UPLOAD SUCCESS =====")
    print("Video ID:", video_id)
    print("https://youtube.com/shorts/" + video_id)


if __name__ == "__main__":
    upload_video()
