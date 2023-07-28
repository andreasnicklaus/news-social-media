import requests
import os

BASE_URL = "https://api.nytimes.com"
API_KEY = API_KEY = os.environ.get("NYT_API_KEY")


def get_most_popular():
    path = "/svc/mostpopular/v2/viewed/1.json"
    response = requests.get(BASE_URL + path, params={"api-key": API_KEY})
    return response.json().get("results")[0]
