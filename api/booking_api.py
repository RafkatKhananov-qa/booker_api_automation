import allure
import requests

from config.secret_config import BASE_URL
from data.payloads import BOOKING_PAYLOAD, UPDATED_BOOKING_PAYLOAD


@allure.step("POST /booking - создать бронь")
def create_booking(
        headers: dict,
        checkin=None,
        checkout=None,
        **kwargs
):
    payload = BOOKING_PAYLOAD.copy()

    payload["bookingdates"] = payload["bookingdates"].copy()

    if checkin:
        payload["bookingdates"]["checkin"] = checkin

    if checkout:
        payload["bookingdates"]["checkout"] = checkout

    payload.update(kwargs)

    return requests.post(
        f"{BASE_URL}/booking",
        headers=headers,
        json=payload
    )


@allure.step("GET /booking - получить список броней")
def get_bookings(firstname=None, lastname=None,
                 checkin=None, checkout=None):
    params = {}

    if firstname:
        params["firstname"] = firstname

    if lastname:
        params["lastname"] = lastname

    if checkin:
        params["checkin"] = checkin

    if checkout:
        params["checkout"] = checkout

    return requests.get(
        f"{BASE_URL}/booking",
        params=params
    )


@allure.step("GET /booking/{booking_id} - получить бронь")
def get_booking(booking_id: int):
    return requests.get(f"{BASE_URL}/booking/{booking_id}")


@allure.step("PUT /booking/{booking_id} - обновить бронь")
def update_booking(booking_id: int, headers: dict, payload: dict = None):
    return requests.put(f"{BASE_URL}/booking/{booking_id}",
                        headers=headers,
                        json=payload or UPDATED_BOOKING_PAYLOAD)


@allure.step("PATCH /booking/{booking_id} - частично обновить бронь")
def patch_booking(booking_id: int, headers: dict, payload: dict = None):
    return requests.patch(f"{BASE_URL}/booking/{booking_id}",
                          headers=headers,
                          json=payload)


@allure.step("DELETE /booking/{booking_id} - удалить бронь")
def delete_booking(booking_id: int, headers: dict):
    return requests.delete(f"{BASE_URL}/booking/{booking_id}",
                           headers=headers)
