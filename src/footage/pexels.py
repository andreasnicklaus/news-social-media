import requests
import os

BASE_URL = "https://api.pexels.com"
API_KEY = os.environ.get("PEXELS_API_KEY")


def get_photos_by_keyword(keyword, n):
    path = "/v1/search"
    response = requests.get(
        BASE_URL + path,
        params={"query": keyword, "orientation": "portrait", "per_page": n, "page": 1},
        headers={"Authorization": API_KEY},
    )
    return response.json().get("photos")


def get_videos_by_keyword(keyword, n):
    path = "/videos/search"
    response = requests.get(
        BASE_URL + path,
        params={"query": keyword, "orientation": "portrait", "per_page": n, "page": 1},
        headers={"Authorization": API_KEY},
    )
    return response.json().get("videos")
