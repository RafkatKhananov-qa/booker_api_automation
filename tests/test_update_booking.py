import allure
import pytest

from api.booking_api import create_booking, update_booking, patch_booking
from data.payloads import (BOOKING_EMPTY_FIRSTNAME_PAYLOAD, UPDATED_BOOKING_PAYLOAD,
                           UPDATED_FIRSTNAME_BOOKING_PAYLOAD, UPDATED_PRICE_BOOKING_PAYLOAD,
                           UPDATED_DEPOSITPAID_BOOKING_PAYLOAD)
from data.schemas import BOOKING_SCHEMA
from utils.assertions import (assert_status_code,
                              assert_field_in_response_message,
                              assert_response_fields)
from jsonschema import validate


@allure.feature("Update Booking")
class TestUpdateBooking:
    @allure.story("Успешное обновление брони")
    @allure.title("Полное обновление брони (PUT) с токеном")
    def test_put_001(self, request_context, auth_token,
                     api_headers, api_headers_with_cookie):
        r = create_booking(request_context, headers=api_headers)
        assert_status_code(r, 200)
        assert_field_in_response_message(r, "bookingid")
        booking_id = r.json()["bookingid"]

        r = update_booking(request_context, booking_id,
                           headers=api_headers_with_cookie(auth_token))
        assert_status_code(r, 200)

        assert_response_fields(r.json(), UPDATED_BOOKING_PAYLOAD)

    @allure.story("Успешное обновление брони")
    @allure.title("Частичное обновление брони (PATCH) с токеном")
    def test_put_002(self, request_context, auth_token,
                     api_headers, api_headers_with_cookie):
        r = create_booking(request_context, headers=api_headers)
        assert_status_code(r, 200)
        assert_field_in_response_message(r, "bookingid")
        booking_id = r.json()["bookingid"]

        r = patch_booking(request_context, booking_id,
                          headers=api_headers_with_cookie(auth_token),
                          payload={"firstname": "Jackson"})
        assert_status_code(r, 200)

        assert_response_fields(r.json(), UPDATED_FIRSTNAME_BOOKING_PAYLOAD)

    @allure.story("Негативные сценарии обновления брони")
    @allure.title("Обновление несуществующей брони")
    def test_put_003(self, request_context, auth_token,
                     api_headers, api_headers_with_cookie):
        r = update_booking(request_context, 999999,
                           headers=api_headers_with_cookie(auth_token))
        assert_status_code(r, 405)

    @allure.story("Негативные сценарии обновления брони")
    @allure.title("Обновление без токена")
    def test_put_004(self, request_context, api_headers):
        r = create_booking(request_context, headers=api_headers)
        assert_status_code(r, 200)
        assert_field_in_response_message(r, "bookingid")
        booking_id = r.json()["bookingid"]

        r = update_booking(request_context, booking_id, headers=api_headers)
        assert_status_code(r, 403)

    @allure.story("Негативные сценарии обновления брони")
    @allure.title("Обновление с неверным токеном")
    def test_put_005(self, request_context, auth_token,
                     api_headers, api_headers_with_cookie):
        r = create_booking(request_context, headers=api_headers)
        assert_status_code(r, 200)
        assert_field_in_response_message(r, "bookingid")
        booking_id = r.json()["bookingid"]

        r = update_booking(request_context, booking_id,
                           headers=api_headers_with_cookie("56d620e8836e02b1"))
        assert_status_code(r, 403)

    @allure.story("Негативные сценарии обновления брони")
    @allure.title("Обновление с невалидными данными")
    def test_put_006(self, request_context, auth_token,
                     api_headers, api_headers_with_cookie):
        r = create_booking(request_context, headers=api_headers)
        assert_status_code(r, 200)
        assert_field_in_response_message(r, "bookingid")
        booking_id = r.json()["bookingid"]

        r = update_booking(request_context, booking_id,
                           headers=api_headers_with_cookie(auth_token),
                           payload=BOOKING_EMPTY_FIRSTNAME_PAYLOAD)
        assert_status_code(r, 200)

        assert_response_fields(r.json(), BOOKING_EMPTY_FIRSTNAME_PAYLOAD)

    @allure.story("Успешное обновление брони")
    @allure.title("Обновление с изменением дат")
    def test_put_007(self, request_context, auth_token,
                     api_headers, api_headers_with_cookie):
        r = create_booking(request_context, headers=api_headers)
        assert_status_code(r, 200)
        assert_field_in_response_message(r, "bookingid")
        booking_id = r.json()["bookingid"]

        r = update_booking(request_context, booking_id,
                           headers=api_headers_with_cookie(auth_token))
        assert_status_code(r, 200)

        assert_response_fields(r.json(), UPDATED_BOOKING_PAYLOAD)

    @allure.story("Успешное обновление брони")
    @allure.title("Валидация схемы после обновления")
    def test_put_008(self, request_context, auth_token,
                     api_headers, api_headers_with_cookie):
        r = create_booking(request_context, headers=api_headers)
        assert_status_code(r, 200)
        assert_field_in_response_message(r, "bookingid")
        booking_id = r.json()["bookingid"]

        r = update_booking(request_context, booking_id,
                           headers=api_headers_with_cookie(auth_token))
        assert_status_code(r, 200)

        assert_response_fields(r.json(), UPDATED_BOOKING_PAYLOAD)
        validate(instance=r.json(), schema=BOOKING_SCHEMA)

    @allure.story("Успешное обновление брони")
    @allure.title("PATCH: обновление только totalprice и depositpaid")
    @pytest.mark.parametrize("payload, field, value", [
        (UPDATED_PRICE_BOOKING_PAYLOAD, "totalprice", 500),
        (UPDATED_DEPOSITPAID_BOOKING_PAYLOAD, "depositpaid", False),
    ])
    def test_patch(self, request_context, auth_token,
                   api_headers, api_headers_with_cookie,
                   payload, field, value):
        r = create_booking(request_context, headers=api_headers)
        assert_status_code(r, 200)
        assert_field_in_response_message(r, "bookingid")
        booking_id = r.json()["bookingid"]

        r = patch_booking(request_context, booking_id,
                          headers=api_headers_with_cookie(auth_token),
                          payload={field: value})
        assert_status_code(r, 200)

        assert_response_fields(r.json(), payload)
