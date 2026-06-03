# AQA Booker API

Автоматизированные тесты для [Restful Booker API](https://restful-booker.herokuapp.com) — учебного REST API для управления бронированием отелей.

## Стек

| Инструмент | Версия | Назначение |
|---|---|---|
| Python | 3.11+ | Язык |
| Pytest | 9.0.3 | Тест-фреймворк |
| Playwright | 1.60.0 | HTTP-клиент для API-запросов |
| Allure | 2.16.0 | Отчётность |
| jsonschema | 4.26.0 | Валидация схем ответов |
| python-dotenv | 1.2.2 | Управление переменными окружения |

## Структура проекта

```
aqa_booker_api/
├── .github/workflows/ci.yml   # GitHub Actions CI/CD
├── api/
│   ├── auth_api.py            # Обёртка над /auth
│   └── booking_api.py         # Обёртка над /booking
├── config/
│   └── secret_config.py       # Base URL и конфигурация среды
├── data/
│   ├── payloads.py            # Тестовые данные
│   └── schemas.py             # JSON-схемы для валидации
├── tests/
│   ├── test_auth.py           # Аутентификация (8 тестов)
│   ├── test_create_booking.py # Создание бронирований (10 тестов)
│   ├── test_get_booking.py    # Получение бронирований (10 тестов)
│   ├── test_update_booking.py # Обновление (PUT/PATCH)
│   ├── test_delete_booking.py # Удаление
│   ├── test_validation.py     # Валидация и негативные сценарии
│   ├── test_e2e.py            # E2E сценарии
│   └── test_perf.py           # Производительность
├── utils/
│   ├── assertions.py          # Кастомные ассерты с Allure-шагами
│   └── logger.py              # Конфигурация логирования
├── conftest.py                # Фикстуры Pytest
├── pytest.ini                 # Конфигурация Pytest
├── requirements.txt           # Зависимости
└── .env                       # Переменные окружения (не коммитить)
```

## Установка

```bash
# Клонировать репозиторий
git clone <repo-url>
cd aqa_booker_api

# Создать и активировать виртуальное окружение
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows

# Установить зависимости
pip install -r requirements.txt

# Установить браузеры Playwright
playwright install
```

## Конфигурация

Создайте файл `.env` в корне проекта:

```env
BOOKER_USERNAME=admin
BOOKER_PASSWORD=password123
```

## Запуск тестов

```bash
# Все тесты
pytest

# Конкретный файл
pytest tests/test_auth.py

# По маркеру
pytest -m smoke
pytest -m regression
pytest -m negative
pytest -m e2e

# С Allure-отчётом
pytest --alluredir=allure-results
allure serve allure-results
```

### Маркеры

| Маркер | Описание |
|---|---|
| `smoke` | Быстрая проверка базовой функциональности |
| `regression` | Полный регрессионный прогон |
| `negative` | Негативные сценарии и обработка ошибок |
| `e2e` | Сквозные сценарии |

## Покрытие

| Файл | Эндпоинт | Метод |
|---|---|---|
| `test_auth.py` | `/auth` | POST |
| `test_create_booking.py` | `/booking` | POST |
| `test_get_booking.py` | `/booking`, `/booking/{id}` | GET |
| `test_update_booking.py` | `/booking/{id}` | PUT, PATCH |
| `test_delete_booking.py` | `/booking/{id}` | DELETE |
| `test_e2e.py` | Все эндпоинты | Полный CRUD |
| `test_perf.py` | Все эндпоинты | Время ответа |
| `test_validation.py` | Все эндпоинты | Валидация |

## Фикстуры

| Фикстура | Scope | Описание |
|---|---|---|
| `request_context` | session | Playwright HTTP-контекст |
| `auth_token` | session | Токен аутентификации |
| `api_headers` | function | Базовые заголовки (`application/json`) |
| `api_headers_with_cookie` | function | Заголовки с токеном для авторизованных запросов |

## CI/CD

GitHub Actions запускает тесты при:
- Push и Pull Request в ветки `main` / `develop`
- Ручном запуске (`workflow_dispatch`)
- По расписанию — ежедневно в 05:00 UTC

После прогона Allure-отчёт публикуется на GitHub Pages, результаты отправляются в Telegram.

Переменные окружения для CI хранятся в GitHub Secrets: `BOOKER_USERNAME`, `BOOKER_PASSWORD`.
