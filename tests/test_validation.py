import allure
import pytest

from playwright.sync_api import Error as PlaywrightError

from api.auth_api import create_token
from api.booking_api import (create_booking, get_bookings,
                             get_booking, update_booking,
                             patch_booking, delete_booking)
from data.payloads import NOT_VALID_PAYLOAD
from data.schemas import BOOKING_SCHEMA, BOOKINGS_LIST_SCHEMA
from utils.assertions import (assert_status_code, assert_array_not_empty,
                              assert_field_in_response_message,
                              assert_response_message,
                              assert_headers_in_response)
from jsonschema import validate


@allure.feature("Validation")
class TestValidation:
    @allure.story("Валидация схемы ответа")
    @allure.title("Валидация схемы ответа создания брони")
    def test_val_001(self, request_context, api_headers):
        r = create_booking(request_context, headers=api_headers)
        assert_status_code(r, 200)
        validate(instance=r.json()["booking"], schema=BOOKING_SCHEMA)

    @allure.story("Валидация схемы ответа")
    @allure.title("Валидация схемы ответа списка броней")
    def test_val_002(self, request_context):
        r = get_bookings(request_context)
        assert_status_code(r, 200)
        assert_array_not_empty(r)
        validate(instance=r.json(), schema=BOOKINGS_LIST_SCHEMA)

    @allure.story("Проверка заголовков ответа")
    @allure.title("Проверка заголовка Content-Type")
    def test_val_003(self, request_context, auth_token,
                     api_headers, api_headers_with_cookie):
        r = create_booking(request_context, headers=api_headers)
        assert_status_code(r, 200)
        assert_field_in_response_message(r, "bookingid")
        booking_id = r.json()["bookingid"]
        assert_headers_in_response(r)

        r = get_booking(request_context, booking_id)
        assert_status_code(r, 200)
        assert_response_message(r, "firstname", "John")
        validate(instance=r.json(), schema=BOOKING_SCHEMA)
        assert_headers_in_response(r)

        r = update_booking(request_context, booking_id,
                           headers=api_headers_with_cookie(auth_token))
        assert_status_code(r, 200)
        assert_response_message(r, "firstname", "Dannie")
        assert_headers_in_response(r)

        r = get_booking(request_context, booking_id)
        assert_status_code(r, 200)
        assert_response_message(r, "firstname", "Dannie")
        assert_headers_in_response(r)

        r = patch_booking(request_context, booking_id,
                          headers=api_headers_with_cookie(auth_token),
                          payload={"totalprice": 500})
        assert_status_code(r, 200)
        assert_response_message(r, "totalprice", 500)
        assert_response_message(r, "firstname", "Dannie")
        assert_headers_in_response(r)

    @allure.story("Проверка времени ответа")
    @allure.title("Время < 2000 мс для всех эндпоинтов")
    def test_val_004(self, request_context, auth_token,
                     api_headers, api_headers_with_cookie):
        r = create_booking(request_context, headers=api_headers)
        assert_status_code(r, 200)
        assert_field_in_response_message(r, "bookingid")
        booking_id = r.json()["bookingid"]

        r = get_booking(request_context, booking_id)
        assert_status_code(r, 200)
        assert_response_message(r, "firstname", "John")
        validate(instance=r.json(), schema=BOOKING_SCHEMA)

        r = update_booking(request_context, booking_id,
                           headers=api_headers_with_cookie(auth_token))
        assert_status_code(r, 200)
        assert_response_message(r, "firstname", "Dannie")

        r = get_booking(request_context, booking_id)
        assert_status_code(r, 200)
        assert_response_message(r, "firstname", "Dannie")

        r = patch_booking(request_context, booking_id,
                          headers=api_headers_with_cookie(auth_token),
                          payload={"totalprice": 500})
        assert_status_code(r, 200)
        assert_response_message(r, "totalprice", 500)
        assert_response_message(r, "firstname", "Dannie")

        r = delete_booking(request_context, booking_id,
                           headers=api_headers_with_cookie(auth_token))
        assert_status_code(r, 201)

        r = get_booking(request_context, booking_id)
        assert_status_code(r, 404)

    @allure.story("Обработка 400 (Bad Request)")
    @allure.title("Отправить невалидный JSON")
    def test_err_001(self, request_context, api_headers):
        r = create_token(
            request_context,
            headers=api_headers,
            data=NOT_VALID_PAYLOAD
        )
        assert_status_code(r, 400)

    @allure.story("Обработка 403 (Forbidden)")
    @allure.title("Запрос к защищённому эндпоинту без токена")
    def test_err_002(self, request_context, api_headers):
        r = create_booking(request_context, headers=api_headers)
        assert_status_code(r, 200)
        assert_field_in_response_message(r, "bookingid")
        booking_id = r.json()["bookingid"]

        r = get_booking(request_context, booking_id)
        assert_status_code(r, 200)
        assert_response_message(r, "firstname", "John")
        validate(instance=r.json(), schema=BOOKING_SCHEMA)

        r = update_booking(request_context, booking_id, headers=api_headers)
        assert_status_code(r, 403)

        r = patch_booking(request_context, booking_id, headers=api_headers,
                          payload={"totalprice": 500})
        assert_status_code(r, 403)

        r = delete_booking(request_context, booking_id, headers=api_headers)
        assert_status_code(r, 403)

    @allure.story("Обработка 404 (Not Found)")
    @allure.title("Запрос несуществующего ресурса")
    def test_err_003(self, request_context):
        r = get_booking(request_context, 465464)
        assert_status_code(r, 404)

    @allure.story("Таймаут запроса")
    @allure.title("Проверка таймаута запроса")
    def test_err_004(self, request_context):
        with pytest.raises(PlaywrightError):
            get_bookings(request_context, timeout=1)
