import requests
import random
import string
from config import SHORT_API, SHORT_URL


def generate_random_alphanumeric():
    """Generate a random 8-letter alphanumeric string."""
    characters = string.ascii_letters + string.digits
    random_chars = ''.join(random.choice(characters) for _ in range(8))
    return random_chars

def get_short(url):
    params = {
        "api": SHORT_API,
        "url": url,
        "alias": generate_random_alphanumeric()
    }
    rget = requests.get(f"https://{SHORT_URL}/api", params=params)
    rjson = rget.json()
    if rjson.get("status") == "success" or rget.status_code == 200:
        return rjson.get("shortenedUrl", url)
    else:
        return url
