import allure

from data.payloads import BOOKING_PAYLOAD, UPDATED_BOOKING_PAYLOAD


@allure.step("POST /booking - создать бронь")
def create_booking(
        request_context,
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

    return request_context.post(
        "/booking",
        headers=headers,
        data=payload
    )


@allure.step("GET /booking - получить список броней")
def get_bookings(request_context, firstname=None, lastname=None,
                 checkin=None, checkout=None, timeout=None):
    params = {}

    if firstname:
        params["firstname"] = firstname

    if lastname:
        params["lastname"] = lastname

    if checkin:
        params["checkin"] = checkin

    if checkout:
        params["checkout"] = checkout

    return request_context.get(
        "/booking",
        params=params,
        timeout=timeout
    )


@allure.step("GET /booking/{booking_id} - получить бронь")
def get_booking(request_context, booking_id: int):
    return request_context.get(f"/booking/{booking_id}")


@allure.step("PUT /booking/{booking_id} - обновить бронь")
def update_booking(request_context, booking_id: int, headers: dict, payload: dict = None):
    return request_context.put(f"/booking/{booking_id}",
                               headers=headers,
                               data=payload or UPDATED_BOOKING_PAYLOAD)


@allure.step("PATCH /booking/{booking_id} - частично обновить бронь")
def patch_booking(request_context, booking_id: int, headers: dict, payload: dict = None):
    return request_context.patch(f"/booking/{booking_id}",
                                 headers=headers,
                                 data=payload)


@allure.step("DELETE /booking/{booking_id} - удалить бронь")
def delete_booking(request_context, booking_id: int, headers: dict):
    return request_context.delete(f"/booking/{booking_id}",
                                  headers=headers)
