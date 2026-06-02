import allure
from jsonschema import validate

from api.booking_api import (create_booking, get_booking, update_booking,
                             patch_booking, delete_booking)

from data.schemas import BOOKING_SCHEMA
from utils.assertions import (assert_status_code, assert_response_message,
                              assert_field_in_response_message)
from utils.logger import logger


@allure.feature("E2E")
class TestE2E:
    @allure.story("Reservation")
    @allure.title("Полный цикл бронирования: авторизация → создание → обновление → удаление")
    def test_e2e_001(self, request_context, auth_token,
                     api_headers, api_headers_with_cookie):
        logger.info("=== Старт теста: test_e2e_001 ===")

        logger.info("Шаг 1: Создание бронирования")
        r = create_booking(request_context, headers=api_headers)
        assert_status_code(r, 200)
        assert_field_in_response_message(r, "bookingid")
        booking_id = r.json()["bookingid"]
        logger.info(f"Бронирование создано, booking_id={booking_id}")

        logger.info(f"Шаг 2: Получение бронирования booking_id={booking_id}")
        r = get_booking(request_context, booking_id)
        assert_status_code(r, 200)
        assert_response_message(r, "firstname", "John")
        validate(instance=r.json(), schema=BOOKING_SCHEMA)
        logger.info(f"Бронирование получено: {r.json()}")

        logger.info(f"Шаг 3: Полное обновление (PUT) booking_id={booking_id}")
        r = update_booking(request_context, booking_id,
                           headers=api_headers_with_cookie(auth_token))
        assert_status_code(r, 200)
        assert_response_message(r, "firstname", "Dannie")
        logger.info(f"Бронирование обновлено: firstname={r.json()['firstname']}")

        logger.info(f"Шаг 4: Проверка обновления GET booking_id={booking_id}")
        r = get_booking(request_context, booking_id)
        assert_status_code(r, 200)
        assert_response_message(r, "firstname", "Dannie")
        logger.info(f"Данные после PUT подтверждены: {r.json()}")

        logger.info(f"Шаг 5: Частичное обновление (PATCH) booking_id={booking_id}")
        r = patch_booking(request_context, booking_id,
                          headers=api_headers_with_cookie(auth_token),
                          payload={"totalprice": 500})
        assert_status_code(r, 200)
        assert_response_message(r, "totalprice", 500)
        assert_response_message(r, "firstname", "Dannie")
        logger.info(f"PATCH выполнен: totalprice={r.json()['totalprice']}")

        logger.info(f"Шаг 6: Удаление бронирования booking_id={booking_id}")
        r = delete_booking(request_context, booking_id,
                           headers=api_headers_with_cookie(auth_token))
        assert_status_code(r, 201)
        logger.info(f"Бронирование удалено, статус={r.status}")

        logger.info(f"Шаг 7: Проверка удаления GET booking_id={booking_id}")
        r = get_booking(request_context, booking_id)
        assert_status_code(r, 404)
        logger.info("Бронирование не найдено (404)")

        logger.info("=== Тест test_e2e_001 завершён успешно ===")
