# promAPItest

`promAPItest` — это проект для автоматизированного тестирования API с использованием Python, pytest, Pydantic и Allure. Проект включает тесты для проверки функциональности эндпоинта `/pet` (на основе Petstore API), обеспечивая валидацию запросов и ответов с использованием Pydantic-моделей и генерацию отчётов с помощью Allure.

## Структура проекта

```
promAPItest/
├── core/
│   ├── __init__.py
│   ├── clients/
│   │   ├── __init__.py
│   │   ├── api_client.py    # Клиент для отправки HTTP-запросов
│   │   ├── endpoints.py     # Перечисления эндпоинтов API
│   ├── models/
│   │   ├── __init__.py
│   │   ├── pet.py           # Pydantic-модели для валидации данных
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── environment.py   # Настройки окружения
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Фикстуры для тестов
│   ├── test_pet.py         # Тесты для эндпоинта /pet
├── .env                    # Файл с переменными окружения
├── requirements.txt         # Зависимости проекта
├── README.md               # Документация проекта
```

## Требования

- Python 3.13
- Node.js (для Allure-отчётов)
- Виртуальное окружение (рекомендуется)

## Установка

1. **Клонируйте репозиторий**:
   ```bash
   git clone https://github.com/zajkovdd/promAPItest.git
   cd promAPItest
   ```

2. **Создайте и активируйте виртуальное окружение**:
   ```bash
   python3.13 -m venv .venv
   source .venv/bin/activate
   ```

3. **Установите зависимости Python из `requirements.txt`**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Установите Allure для генерации отчётов**:
   ```bash
   npm install -g allure-commandline
   ```

5. **Настройте переменные окружения**:
   Создайте файл `.env` в корне проекта со следующим содержимым:
   ```
   ENVIRONMENT=TEST
   TEST_BASE_URL=http://5.181.109.28:9090/api/v3
   ```
   Замените `TEST_BASE_URL` на актуальный URL вашего API, если необходимо.

## Запуск тестов

1. **Запустите тесты с генерацией Allure-результатов**:
   ```bash
   python3.13 -m pytest tests/test_pet.py -v --alluredir=reports
   ```

2. **Просмотрите Allure-отчёт**:
   ```bash
   allure serve reports
   ```

   Это откроет отчёт в вашем веб-браузере.

3. **Очистка старых отчётов** (опционально):
   ```bash
   rm -rf reports
   ```

## Описание тестов

Тесты в `tests/test_pet.py` проверяют функциональность эндпоинта `/pet`:
- **Позитивный тест** (`test_add_new_pet`): Проверяет успешное создание питомца с валидными данными.
- Используются Pydantic-модели для валидации запросов и ответов.
- Логирование шагов и ошибок осуществляется через Allure.

## Пример теста

```python
@allure.title('Позитивный тест: добавление нового питомца')
@allure.description('Проверяет успешное создание нового питомца через эндпоинт /pet с валидными данными.')
def test_add_new_pet(api_client):
    payload = Pet(
        id=1,
        name="Buddy",
        category=Category(id=1, name="Dogs"),
        photoUrls=["https://example.com/pet1.jpg"],
        tags=["friendly"],
        status=PetStatus.AVAILABLE
    )
    response = api_client.post(PetEndpoints.PET_ENDPOINT.value, data=payload.dict(), status_code=200)
    response_data = Pet(**response)
    assert response_data.id == payload.id
    assert response_data.name == payload.name
    assert response_data.status == payload.status
    assert response_data.category.name == payload.category.name
```

## Устранение проблем

- **ModuleNotFoundError: No module named 'core'**:
  - Убедитесь, что вы запускаете тесты из корня проекта:
    ```bash
    cd /path/to/promAPItest
    python3.13 -m pytest tests/test_pet.py -v --alluredir=reports
    ```
  - Проверьте наличие файлов `__init__.py` в папках `core`, `core/clients`, `core/models`, `core/settings`, и `tests`.
  - Добавьте корень проекта в `PYTHONPATH`, если необходимо:
    ```bash
    export PYTHONPATH=$PYTHONPATH:/path/to/promAPItest
    ```

- **Ошибка `allure: command not found`**:
  - Убедитесь, что `allure-commandline` установлен:
    ```bash
    npm install -g allure-commandline
    allure --