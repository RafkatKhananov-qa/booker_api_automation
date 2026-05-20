import allure
from jsonschema import validate

from api.auth_api import create_token
from api.booking_api import (create_booking, get_booking, update_booking,
                             patch_booking, delete_booking)

from data.schemas import BOOKING_SCHEMA
from utils.assertions import (assert_status_code, assert_response_message,
                              assert_field_in_response_message,
                              assert_response_time)
from utils.logger import logger


@allure.feature("E2E")
class TestE2E:
    @allure.story("Reservation")
    @allure.title("Полный цикл бронирования: авторизация → создание → обновление → удаление")
    def test_e2e_001(self, api_headers, api_headers_with_cookie):
        logger.info("=== Старт теста: test_e2e_001 ===")

        logger.info("Шаг 1: Авторизация")
        r = create_token(headers=api_headers)
        assert_status_code(r, 200)
        assert_field_in_response_message(r, "token")
        token = r.json()["token"]
        logger.info(f"Токен получен: {token}")

        logger.info("Шаг 2: Создание бронирования")
        r = create_booking(headers=api_headers)
        assert_status_code(r, 200)
        assert_field_in_response_message(r, "bookingid")
        booking_id = r.json()["bookingid"]
        logger.info(f"Бронирование создано, booking_id={booking_id}")

        logger.info(f"Шаг 3: Получение бронирования booking_id={booking_id}")
        r = get_booking(booking_id)
        assert_status_code(r, 200)
        assert_response_message(r, "firstname", "John")
        validate(instance=r.json(), schema=BOOKING_SCHEMA)
        logger.info(f"Бронирование получено: {r.json()}")

        logger.info(f"Шаг 4: Полное обновление (PUT) booking_id={booking_id}")
        r = update_booking(booking_id, headers=api_headers_with_cookie(token))
        assert_status_code(r, 200)
        assert_response_message(r, "firstname", "Dannie")
        logger.info(f"Бронирование обновлено: firstname={r.json()['firstname']}")

        logger.info(f"Шаг 5: Проверка обновления GET booking_id={booking_id}")
        r = get_booking(booking_id)
        assert_status_code(r, 200)
        assert_response_message(r, "firstname", "Dannie")
        logger.info(f"Данные после PUT подтверждены: {r.json()}")

        logger.info(f"Шаг 6: Частичное обновление (PATCH) booking_id={booking_id}")
        r = patch_booking(booking_id, headers=api_headers_with_cookie(token),
                          payload={"totalprice": 500})
        assert_status_code(r, 200)
        assert_response_message(r, "totalprice", 500)
        assert_response_message(r, "firstname", "Dannie")
        logger.info(f"PATCH выполнен: totalprice={r.json()['totalprice']}")

        logger.info(f"Шаг 7: Удаление бронирования booking_id={booking_id}")
        r = delete_booking(booking_id, headers=api_headers_with_cookie(token))
        assert_status_code(r, 201)
        logger.info(f"Бронирование удалено, статус={r.status_code}")

        logger.info(f"Шаг 8: Проверка удаления GET booking_id={booking_id}")
        r = get_booking(booking_id)
        assert_status_code(r, 404)
        assert_response_time(r, 2.0)
        logger.info(f"Бронирование не найдено (404), время ответа={r.elapsed.total_seconds():.3f}s")

        logger.info("=== Тест test_e2e_001 завершён успешно ===")
