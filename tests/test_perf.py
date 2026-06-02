import time

import allure

from api.auth_api import create_token
from api.booking_api import (get_bookings, create_booking,
                             update_booking, patch_booking,
                             delete_booking)
from utils.assertions import (assert_status_code,
                              assert_field_in_response_message,
                              assert_response_message)


@allure.feature("Performance")
class TestPerformance:
    @allure.story("Нагрузочный тест: 10 последовательных запросов")
    @allure.title("Замер времени 10 GET-запросов подряд")
    def test_perf_001(self, request_context, api_headers):
        response_times = []

        for i in range(10):
            start_time = time.time()

            r = get_bookings(request_context)

            end_time = time.time()

            response_time_ms = (end_time - start_time) * 1000
            response_times.append(response_time_ms)

            print(f"Request #{i + 1}: {response_time_ms:.2f} ms")

            assert_status_code(r, 200)

        average_time = sum(response_times) / len(response_times)

        print(f"\nAverage response time: {average_time:.2f} ms")

        assert average_time < 2000, \
            f"Average response time is too high: {average_time:.2f} ms"

    @allure.story("Тест на идемпотентность получения токена")
    @allure.title("Два раза POST /auth → оба токена работают")
    def test_perf_002(self, request_context, auth_token,
                      api_headers, api_headers_with_cookie):
        r = create_token(request_context, headers=api_headers)
        assert_status_code(r, 200)
        assert_field_in_response_message(r, "token")
        token_1 = r.json()["token"]

        r = create_token(request_context, headers=api_headers)
        assert_status_code(r, 200)
        assert_field_in_response_message(r, "token")
        token_2 = r.json()["token"]

        r = create_booking(request_context, headers=api_headers)
        assert_status_code(r, 200)
        assert_field_in_response_message(r, "bookingid")
        booking_id_1 = r.json()["bookingid"]

        r = create_booking(request_context, headers=api_headers)
        assert_status_code(r, 200)
        assert_field_in_response_message(r, "bookingid")
        booking_id_2 = r.json()["bookingid"]

        r = update_booking(request_context, booking_id_1,
                           headers=api_headers_with_cookie(token_1))
        assert_status_code(r, 200)
        assert_response_message(r, "firstname", "Dannie")

        r = update_booking(request_context, booking_id_2,
                           headers=api_headers_with_cookie(token_2))
        assert_status_code(r, 200)
        assert_response_message(r, "firstname", "Dannie")

        r = patch_booking(request_context, booking_id_1,
                          headers=api_headers_with_cookie(token_1),
                          payload={"totalprice": 500})
        assert_status_code(r, 200)
        assert_response_message(r, "totalprice", 500)
        assert_response_message(r, "firstname", "Dannie")

        r = patch_booking(request_context, booking_id_2,
                          headers=api_headers_with_cookie(token_2),
                          payload={"totalprice": 500})
        assert_status_code(r, 200)
        assert_response_message(r, "totalprice", 500)
        assert_response_message(r, "firstname", "Dannie")

        r = delete_booking(request_context, booking_id_1,
                           headers=api_headers_with_cookie(token_1))
        assert_status_code(r, 201)

        r = delete_booking(request_context, booking_id_2,
                           headers=api_headers_with_cookie(token_2))
        assert_status_code(r, 201)
