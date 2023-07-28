import requests
import os

BASE_URL = " https://newsapi.org"
API_KEY = os.environ.get("NEWS_API_KEY")


def get_all():
    path = "/v2/top-headlines"
    response = requests.get(
        BASE_URL + path, params={"country": "us", "apiKey": API_KEY}
    )
    return response.json().get("articles")[0]
