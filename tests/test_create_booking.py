import allure

from api.booking_api import create_booking, get_booking
from data.schemas import BOOKING_SCHEMA
from utils.assertions import (assert_status_code,
                              assert_field_in_response_message,
                              assert_field_value_type)
from jsonschema import validate


@allure.feature("Create Booking")
class TestCreateBooking:
    @allure.story("Успешное создание брони")
    @allure.title("Создание валидной брони")
    def test_post_001(self, request_context, api_headers):
        r = create_booking(request_context, headers=api_headers)
        assert_status_code(r, 200)
        assert_field_in_response_message(r, "bookingid")
        assert_field_value_type(r, "bookingid", int)

    @allure.story("Успешное создание брони")
    @allure.title("Создание брони с минимальными полями")
    def test_post_002(self, request_context, api_headers):
        r = create_booking(request_context, headers=api_headers)
        assert_status_code(r, 200)

    @allure.story("Успешное создание брони")
    @allure.title("Создание брони с depositpaid=false")
    def test_post_003(self, request_context, api_headers):
        r = create_booking(request_context, api_headers, depositpaid=False)
        assert_status_code(r, 200)
        assert r.json()["booking"]["depositpaid"] is False

    @allure.story("Успешное создание брони")
    @allure.title("Создание брони с additionalneeds")
    def test_post_004(self, request_context, api_headers):
        r = create_booking(request_context, api_headers, additionalneeds="Breakfast")
        assert_status_code(r, 200)
        assert r.json()["booking"]["additionalneeds"] == "Breakfast"

    @allure.story("Негативные сценарии создания брони")
    @allure.title("Создание брони с checkout раньше checkin")
    def test_post_005(self, request_context, api_headers):
        r = create_booking(request_context, api_headers,
                           checkin="2026-05-07", checkout="2026-05-01")
        assert_status_code(r, 200)
        assert r.json()["booking"]["bookingdates"]["checkin"] == "2026-05-07"
        assert r.json()["booking"]["bookingdates"]["checkout"] == "2026-05-01"

    @allure.story("Негативные сценарии создания брони")
    @allure.title("Создание брони с пустым firstname")
    def test_post_006(self, request_context, api_headers):
        r = create_booking(request_context, api_headers, firstname="")
        assert_status_code(r, 200)
        assert r.json()["booking"]["firstname"] == ""

    @allure.story("Негативные сценарии создания брони")
    @allure.title("Создание брони с превышением лимита lastname")
    def test_post_007(self, request_context, api_headers):
        r = create_booking(request_context, api_headers, lastname="A" * 102255)
        assert_status_code(r, 413)

    @allure.story("Валидация и проверка данных брони")
    @allure.title("Валидация схемы созданной брони")
    def test_post_008(self, request_context, api_headers):
        r = create_booking(request_context, headers=api_headers)
        assert_status_code(r, 200)
        validate(instance=r.json()["booking"], schema=BOOKING_SCHEMA)

    @allure.story("Валидация и проверка данных брони")
    @allure.title("Проверка уникальности bookingid")
    def test_post_009(self, request_context, api_headers):
        r = create_booking(request_context, headers=api_headers)
        assert_status_code(r, 200)
        booking_id_1 = r.json()["bookingid"]

        r = create_booking(request_context, headers=api_headers)
        assert_status_code(r, 200)
        booking_id_2 = r.json()["bookingid"]

        assert booking_id_1 != booking_id_2

    @allure.story("Успешное создание брони")
    @allure.title("Проверка, что созданная бронь доступна по GET")
    def test_post_010(self, request_context, api_headers):
        r = create_booking(request_context, headers=api_headers)
        assert_status_code(r, 200)
        booking_id = r.json()["bookingid"]

        r = get_booking(request_context, booking_id)
        assert_status_code(r, 200)
        validate(instance=r.json(), schema=BOOKING_SCHEMA)
