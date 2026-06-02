import allure

from api.auth_api import create_token
from api.booking_api import create_booking, get_booking, update_booking
from utils.assertions import (assert_status_code, assert_field_in_response_message,
                              assert_response_message,
                              assert_field_not_in_response_message,
                              assert_field_value_type)


@allure.feature("Auth")
class TestAuth:
    @allure.story("Успешная авторизация")
    @allure.title("Получение токена с валидными данными")
    def test_auth_001(self, api_headers, request_context):
        r = create_token(headers=api_headers, request_context=request_context)
        assert_status_code(r, 200)
        assert_field_in_response_message(r, "token")

    @allure.story("Негативные сценарии авторизации")
    @allure.title("Получение токена с неверным паролем")
    def test_auth_002(self, api_headers, request_context):
        r = create_token(headers=api_headers, password="wrongpass", request_context=request_context)
        assert_status_code(r, 200)
        assert_response_message(r, "reason", "Bad credentials")
        assert_field_not_in_response_message(r, "token")

    @allure.story("Негативные сценарии авторизации")
    @allure.title("Получение токена с несуществующим пользователем")
    def test_auth_003(self, api_headers, request_context):
        r = create_token(headers=api_headers, username="fakeuser", request_context=request_context)
        assert_status_code(r, 200)
        assert_response_message(r, "reason", "Bad credentials")
        assert_field_not_in_response_message(r, "token")

    @allure.story("Успешная авторизация")
    @allure.title("Использование токена для защищённого запроса")
    def test_auth_004(self, api_headers, auth_token,
                      api_headers_with_cookie, request_context):
        r = create_booking(headers=api_headers, request_context=request_context)
        assert_status_code(r, 200)
        assert_field_in_response_message(r, "bookingid")
        booking_id = r.json()["bookingid"]

        r = get_booking(request_context, booking_id)
        assert_status_code(r, 200)
        assert_response_message(r, "firstname", "John")

        r = update_booking(request_context, booking_id,
                           headers=api_headers_with_cookie(auth_token))
        assert_status_code(r, 200)
        assert_response_message(r, "firstname", "Dannie")

        r = get_booking(request_context, booking_id)
        assert_status_code(r, 200)
        assert_response_message(r, "firstname", "Dannie")

    @allure.story("Негативные сценарии авторизации")
    @allure.title("Использование неверного токена")
    def test_auth_005(self, api_headers, api_headers_with_cookie, request_context):
        r = create_booking(headers=api_headers, request_context=request_context)
        assert_status_code(r, 200)
        assert_field_in_response_message(r, "bookingid")
        booking_id = r.json()["bookingid"]

        r = get_booking(request_context, booking_id)
        assert_status_code(r, 200)
        assert_response_message(r, "firstname", "John")

        r = update_booking(request_context, booking_id,
                           headers=api_headers_with_cookie("45547"))
        assert_status_code(r, 403)

    @allure.story("Негативные сценарии авторизации")
    @allure.title("Запрос без токена к защищённому эндпоинту")
    def test_auth_006(self, api_headers, request_context):
        r = create_booking(headers=api_headers, request_context=request_context)
        assert_status_code(r, 200)
        assert_field_in_response_message(r, "bookingid")
        booking_id = r.json()["bookingid"]

        r = get_booking(request_context, booking_id)
        assert_status_code(r, 200)
        assert_response_message(r, "firstname", "John")

        r = update_booking(request_context, booking_id, headers=api_headers)
        assert_status_code(r, 403)

    @allure.story("Успешная авторизация")
    @allure.title("Валидация формата токена")
    def test_auth_007(self, api_headers, request_context):
        r = create_token(headers=api_headers, request_context=request_context)
        assert_status_code(r, 200)
        assert_field_in_response_message(r, "token")
        assert_field_value_type(r, "token", str)

    @allure.story("Успешная авторизация")
    @allure.title("Повторное получение токена (идемпотентность)")
    def test_auth_008(self, api_headers, request_context):
        r = create_token(headers=api_headers, request_context=request_context)
        assert_status_code(r, 200)
        assert_field_in_response_message(r, "token")
        assert_field_value_type(r, "token", str)
        token_1 = r.json()["token"]

        r = create_token(headers=api_headers, request_context=request_context)
        assert_status_code(r, 200)
        assert_field_in_response_message(r, "token")
        assert_field_value_type(r, "token", str)
        token_2 = r.json()["token"]

        assert token_1 != token_2
