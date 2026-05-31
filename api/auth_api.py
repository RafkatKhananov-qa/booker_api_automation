import allure
import os

from dotenv import load_dotenv

load_dotenv()


@allure.step("POST /auth - создание токена для пользователя: {username}")
def create_token(
        request_context,
        headers,
        username=None,
        password=None,
        data=None,
):
    return request_context.post(
        "/auth",
        headers=headers,
        data=data or {
            "username": username or os.getenv("BOOKER_USERNAME"),
            "password": password or os.getenv("BOOKER_PASSWORD")
        }
    )
