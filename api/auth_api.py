import requests
import os

from dotenv import load_dotenv

from config.secret_config import BASE_URL

load_dotenv()


def create_token(headers, username=None, password=None):
    return requests.post(f"{BASE_URL}/auth",
                         headers=headers,
                         json={"username": username or os.getenv("BOOKER_USERNAME"),
                               "password": password or os.getenv("BOOKER_PASSWORD")})
