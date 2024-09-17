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
        headers={"Authorization": API_KEY, "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"},
    )
    return response.json().get("videos")
