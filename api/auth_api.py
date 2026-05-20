import allure
import requests
import os

from dotenv import load_dotenv

from config.secret_config import BASE_URL

load_dotenv()


@allure.step("POST /auth - создание токена для пользователя: {username}")
def create_token(
        headers,
        username=None,
        password=None,
        data=None,
        json=None
):
    return requests.post(
        f"{BASE_URL}/auth",
        headers=headers,
        data=data,
        json=json or {
            "username": username or os.getenv("BOOKER_USERNAME"),
            "password": password or os.getenv("BOOKER_PASSWORD")
        }
    )
