import os
import requests
import gzip
import brotli
import zstd
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
        self._set_session_headers()

    def _set_session_headers(self):
        """Установка заголовков и cookies из GET-запроса к promminer.ru."""
        try:
            # Выполняем GET-запрос для получения cookies
            response = requests.get("https://promminer.ru", verify=False)
            cookies = response.cookies.get_dict()
            if not cookies:
                print("Предупреждение: Cookies не получены из ответа promminer.ru")
            else:
                print("Полученные cookies:", cookies)

            # Преобразуем cookies в строку для заголовка Cookie
            cookie_string = "; ".join(f"{key}={value}" for key, value in cookies.items())

            # Установка заголовков
            provided_headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
                "Accept": "application/json",
                "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Content-Type": "application/json",
                "Cookie": cookie_string
            }

            # Установка заголовков в сессию
            self.session.headers.update(provided_headers)
            print("Установленные заголовки в сессию:", dict(self.session.headers))

            # Установка cookies в объект RequestsCookieJar
            self.session.cookies.update(cookies)
            print("Установленные cookies в сессию:", cookies)

        except requests.RequestException as e:
            print(f"Ошибка при получении cookies: {e}")
            raise

    def refresh_session_cookies(self):
        """Обновление cookies через GET-запрос к promminer.ru."""
        try:
            response = self.session.get("https://promminer.ru", verify=False)
            cookies = response.cookies.get_dict()
            self.session.cookies.update(cookies)
            # Обновляем заголовок Cookie
            cookie_string = "; ".join(f"{key}={value}" for key, value in cookies.items())
            self.session.headers.update({"Cookie": cookie_string})
            print("Обновленные cookies:", cookies)
            print("Обновленный заголовок Cookie:", cookie_string)
            return cookies
        except requests.RequestException as e:
            print(f"Ошибка при обновлении cookies: {e}")
            raise

    def get_base_url(self, environment: Environment) -> str:
        if environment == Environment.TEST:
            return os.getenv('TEST_BASE_URL')
        elif environment == Environment.PROD:
            return os.getenv('PROD_BASE_URL')
        else:
            raise ValueError(f'Unsupported environment: {environment}')

    def get(self, endpoint, params=None, status_code=200):
        url = self.base_url + endpoint
        headers = {"Accept": "application/json"}
        response = self.session.get(url, params=params, headers=headers)
        if status_code:
            assert response.status_code == status_code, (
                f"Ожидался код состояния {status_code}, получен {response.status_code}"
            )

        # Попытка ручного декодирования сжатого ответа
        content_encoding = response.headers.get("Content-Encoding")
        if content_encoding == "gzip":
            try:
                response._content = gzip.decompress(response.content)
            except gzip.BadGzipFile:
                pass
        elif content_encoding == "br":
            try:
                response._content = brotli.decompress(response.content)
            except brotli.error:
                pass
        elif content_encoding == "zstd":
            try:
                response._content = zstd.decompress(response.content)
            except zstd.ZstdError:
                pass

        return response

    def post(self, endpoint, json=None, status_code=200):
        url = self.base_url + endpoint
        headers = {"Accept": "application/json"}
        response = self.session.post(url, json=json, headers=headers, verify=False)
        if status_code:
            assert response.status_code == status_code, (
                f"Ожидался код состояния {status_code}, получен {response.status_code}"
            )

        # Попытка ручного декодирования сжатого ответа
        content_encoding = response.headers.get("Content-Encoding")
        if content_encoding == "gzip":
            try:
                response._content = gzip.decompress(response.content)
            except gzip.BadGzipFile:
                pass
        elif content_encoding == "br":
            try:
                response._content = brotli.decompress(response.content)
            except brotli.error:
                pass
        elif content_encoding == "zstd":
            try:
                response._content = zstd.decompress(response.content)
            except zstd.ZstdError:
                pass

        return response