import allure
import pytest
from pydantic import ValidationError
from requests import HTTPError
from tests.conftest import api_client
from core.clients.endpoints import PetEndpoints
from core.models.pet import Pet, PetStatus, Category, Tag

@allure.title('Позитивный тест: добавление нового питомца')
@allure.description('Проверяет успешное создание нового питомца через эндпоинт /pet с валидными данными.')
def test_add_new_pet(api_client):
    # Подготовка данных для отправки
    with allure.step('Создание данных для отправки'):
        payload = Pet(
            id=1,
            name="Buddy",
            category=Category(id=1, name="Dogs"),
            photoUrls=["https://example.com/pet1.jpg"],
            tags=[Tag(id=1, name="friendly")],
            status=PetStatus.AVAILABLE
        )

    # Отправка запроса на добавление питомца
    with allure.step('Отправка POST-запроса для добавления питомца'):
        try:
            response = api_client.post(
                endpoint=PetEndpoints.PET_ENDPOINT.value,  # Используем .value для получения строки
                data=payload.model_dump(),  # Преобразуем Pydantic-модель в словарь
                status_code=200
            )
        except HTTPError as e:
            allure.attach(str(e), name="HTTPError", attachment_type=allure.attachment_type.TEXT)
            pytest.fail(f"Не удалось добавить питомца: {str(e)}")

    # Валидация структуры ответа
    with allure.step('Проверка структуры ответа'):
        try:
            response_data = Pet(**response)  # Валидируем ответ как Pydantic-модель
            assert response_data.id == payload.id, f"Ожидался ID питомца {payload.id}, получено {response_data.id}"
            assert response_data.name == payload.name, f"Ожидалось имя питомца {payload.name}, получено {response_data.name}"
            assert response_data.status == payload.status, f"Ожидался статус {payload.status}, получено {response_data.status}"
            assert response_data.category.name == payload.category.name, \
                f"Ожидалось имя категории {payload.category.name}, получено {response_data.category.name}"
        except ValidationError as e:
            allure.attach(str(e), name="ValidationError", attachment_type=allure.attachment_type.TEXT)
            pytest.fail(f"Ошибка валидации ответа: {str(e)}")

    return response

@allure.title('Получение списка питомцев по статусу')
@allure.description('Проверяет эндпоинт /pet/findByStatus для различных статусов питомцев.')
@pytest.mark.parametrize(
    'status, expected_status_code',
    [
        ('available', 200),
        ('pending', 200),
        ('sold', 200),
        ('reserved', 400),
        ('', 400)
    ]
)
def test_get_list_of_pets_by_status(api_client, create_pet, status, expected_status_code, created_pet_ids=None):
    # Создание питомца для валидных статусов
    if status in [PetStatus.AVAILABLE.value, PetStatus.PENDING.value, PetStatus.SOLD.value]:
        with allure.step(f'Создание питомца со статусом {status} перед запросом'):
            create_pet(PetStatus(status))

    # Отправка запроса на получение списка питомцев
    with allure.step(f'Отправка GET-запроса для получения списка питомцев со статусом {status}'):
        try:
            response = api_client.get(
                endpoint=PetEndpoints.PET_BY_STATUS.value,
                params={'status': status},
                status_code=expected_status_code
            )
        except AssertionError as e:
            allure.attach(str(e), name="AssertionError", attachment_type=allure.attachment_type.TEXT)
            pytest.fail(f"Неожиданный код ответа: {str(e)}")

    # Проверка формата ответа
    with allure.step('Проверка кода ответа и формата данных'):
        if expected_status_code == 200:
            try:
                # Валидация ответа как списка объектов Pet
                pets = [Pet(**item) for item in response]
                assert isinstance(response, list), 'Ответ не является списком'
                assert all(isinstance(pet, Pet) for pet in pets), 'Элементы ответа не соответствуют модели Pet'
            except ValidationError as e:
                allure.attach(str(e), name="ValidationError", attachment_type=allure.attachment_type.TEXT)
                pytest.fail(f"Ошибка валидации ответа: {str(e)}")
        elif expected_status_code == 400:
            assert isinstance(response, dict), 'Ответ не является словарем'


@allure.title('Удаление питомца по ID')
@allure.description('Проверяет успешное удаление питомца через эндпоинт /pet/{petId} и подтверждает, что питомец больше не существует.')
def test_delete_pet_with_id(api_client, create_pet):
    # Создание питомца
    with allure.step('Создание питомца для удаления'):
        response = create_pet(PetStatus.AVAILABLE)
        pet_id = response['id']

    # Отправка запроса на удаление питомца
    with allure.step(f'Отправка DELETE-запроса для удаления питомца с ID {pet_id}'):
        try:
            response = api_client.delete(
                endpoint=f'{PetEndpoints.PET_ENDPOINT.value}/{pet_id}',
                status_code=200
            )
            # Необязательно: проверяем, что ответ содержит ожидаемый текст
            assert response == "Pet deleted", f"Ожидался ответ 'Pet deleted', получено: {response}"
        except AssertionError as e:
            allure.attach(str(e), name="AssertionError", attachment_type=allure.attachment_type.TEXT)
            pytest.fail(f"Не удалось удалить питомца с ID {pet_id}: {str(e)}")

    # Проверка, что питомец удалён
    with allure.step(f'Проверка, что питомец с ID {pet_id} больше не существует'):
        try:
            api_client.get_after_delete(
                endpoint=f'{PetEndpoints.PET_ENDPOINT.value}/{pet_id}',
                status_code=404
            )
        except AssertionError as e:
            allure.attach(str(e), name="AssertionError", attachment_type=allure.attachment_type.TEXT)
            pytest.fail(f"Питомец с ID {pet_id} всё ещё существует: {str(e)}")