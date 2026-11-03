import requests


def build_request_url():
    # без реального відправлення запиту, тому працює й без інтернету
    req = requests.Request("GET", "https://example.com/search",
                           params={"q": "python", "page": 2})
    return req.prepare().url