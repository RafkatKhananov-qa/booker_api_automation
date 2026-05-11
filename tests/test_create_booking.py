from api.booking_api import create_booking, get_booking
from data.schemas import BOOKING_SCHEMA
from utils.assertions import (assert_status_code,
                              assert_field_in_response_message,
                              assert_field_value_type)
from jsonschema import validate


def test_post_001(api_headers):
    r = create_booking(headers=api_headers)
    assert_status_code(r, 200)
    assert_field_in_response_message(r, "bookingid")
    assert_field_value_type(r, "bookingid", int)


def test_post_002(api_headers):
    r = create_booking(headers=api_headers)
    assert_status_code(r, 200)


def test_post_003(api_headers):
    r = create_booking(api_headers, depositpaid=False)
    assert_status_code(r, 200)
    assert r.json()["booking"]["depositpaid"] is False


def test_post_004(api_headers):
    r = create_booking(api_headers, additionalneeds="Breakfast")
    assert_status_code(r, 200)
    assert r.json()["booking"]["additionalneeds"] == "Breakfast"


def test_post_005(api_headers):
    r = create_booking(api_headers, checkin="2026-05-07", checkout="2026-05-01")
    assert_status_code(r, 200)
    assert r.json()["booking"]["bookingdates"]["checkin"] == "2026-05-07"
    assert r.json()["booking"]["bookingdates"]["checkout"] == "2026-05-01"


def test_post_006(api_headers):
    r = create_booking(api_headers, firstname="")
    assert_status_code(r, 200)
    assert r.json()["booking"]["firstname"] == ""


def test_post_007(api_headers):
    r = create_booking(api_headers, lastname="A"*102255)
    assert_status_code(r, 413)


def test_post_008(api_headers):
    r = create_booking(headers=api_headers)
    assert_status_code(r, 200)
    validate(instance=r.json()["booking"], schema=BOOKING_SCHEMA)


def test_post_009(api_headers):
    r = create_booking(headers=api_headers)
    assert_status_code(r, 200)
    booking_id_1 = r.json()["bookingid"]

    r = create_booking(headers=api_headers)
    assert_status_code(r, 200)
    booking_id_2 = r.json()["bookingid"]

    assert booking_id_1 != booking_id_2


def test_post_010(api_headers):
    r = create_booking(headers=api_headers)
    assert_status_code(r, 200)
    booking_id = r.json()["bookingid"]

    r = get_booking(booking_id)
    assert_status_code(r, 200)
    validate(instance=r.json(), schema=BOOKING_SCHEMA)
