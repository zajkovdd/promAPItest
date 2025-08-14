import requests
import os
from dotenv import load_dotenv


from core.settings.environment import Environment

load_dotenv()

class APIClient:
    def __init__(self):
        environment_str = os.getenv('ENVIRONMENT')
        try:
            environment = Environment[environment_str]
        except KeyError:
            raise ValueError(f'Unsupported environment value: {environment_str}')

        self.base_url = self.get_base_url(environment)
        self.session = requests.Session()


    def get_base_url(self, environment: Environment) -> str:
        if environment == Environment.TEST:
            return os.getenv('TEST_BASE_URL')
        elif environment == Environment.PROD:
            return os.getenv('PROD_BASE_URL')
        else:
            raise ValueError(f'Unsupported environment: {environment}')

    def get(self, endpoint, params=None, status_code=200):
        url = self.base_url + endpoint
        response = self.session.get(url, params=params)
        if status_code:
            assert response.status_code == status_code
        return response.json()

    def post(self, endpoint, data=None, status_code=200):
        url = self.base_url + endpoint
        response = self.session.post(url, json=data)
        if status_code:
            assert response.status_code == status_code
        return response.json()

    def delete(self, endpoint, status_code=None):
        response = self.session.delete(f"{self.base_url}{endpoint}")
        if status_code is not None:
            assert response.status_code == status_code, (
                f"Expected status code {status_code}, but got {response.status_code}. "
                f"Response: {response.text}"
            )
        return response.text  # Возвращаем текст для не-JSON ответов

    def get_after_delete(self, endpoint, params=None, status_code=200):
        url = self.base_url + endpoint
        response = self.session.get(url, params=params)
        if status_code:
            assert response.status_code == status_code
        return response.text


