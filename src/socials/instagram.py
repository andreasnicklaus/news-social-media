import requests
import json
import time
import os

PROFILE_ID = 17841460807049935
IG_ACCESS_TOKEN = os.environ.get("IG_ACCESS_TOKEN")
WAIT_SECONDS_BETWEEN_MEDIA_CREATION_AND_PUBLISHING = 10
PUBLISHING_TRIES = 10


def post(file_path, caption):
    url = upload_publicly(file_path)
    print(url)
    container_id = create_media_container(url, caption)
    print(container_id)
    result = publish_media_container(container_id)
    print(result)


def upload_publicly(file_path):
    url = "https://tmpfiles.org/api/v1/upload"

    payload = {}
    files = [
        (
            "file",
            (
                file_path.split("/")[-1],
                open(file_path, "rb"),
                "application/octet-stream",
            ),
        )
    ]
    headers = {}
    page_url = (
        json.loads(
            requests.request(
                "POST", url, headers=headers, data=payload, files=files
            ).text
        )
        .get("data")
        .get("url")
    )
    return f'https://tmpfiles.org/dl/{"/".join(page_url.split("/")[-2:])}'


def create_media_container(public_url, caption):
    return (
        requests.post(
            f"https://graph.facebook.com/{PROFILE_ID}/media",
            params={
                "video_url": public_url,
                "caption": caption,
                "media_type": "REELS",
                "access_token": IG_ACCESS_TOKEN,
            },
        )
        .json()
        .get("id")
    )


def publish_media_container(container_id, iteration=1):
    time.sleep(WAIT_SECONDS_BETWEEN_MEDIA_CREATION_AND_PUBLISHING)
    status_check = requests.get(
        f"https://graph.facebook.com/{container_id}/",
        params={
            "fields": ["status,status_code"],
            "access_token": IG_ACCESS_TOKEN,
        },
    ).json()

    if status_check.get("status_code") == "FINISHED":
        return requests.post(
            f"https://graph.facebook.com/{PROFILE_ID}/media_publish",
            params={
                "creation_id": container_id,
                "access_token": IG_ACCESS_TOKEN,
            },
        ).json()
    elif iteration >= PUBLISHING_TRIES:
        raise Exception(f"Publishing ended after {PUBLISHING_TRIES} iterations")
    elif status_check.get("status_code") == "IN_PROGRESS":
        print(f"trying again, iteration {iteration}")
        return publish_media_container(container_id, iteration=iteration + 1)
    elif status_check.get("status_code") == "ERROR":
        raise Exception(f"status ERROR: {status_check.get('status')}")
