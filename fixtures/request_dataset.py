import requests
from rest_framework import status


class RequestException(BaseException):
    def __init__(self, error: status):
        self.status = error


def request(url: str):
    result = None
    status_code = None

    try:
        response = requests.get(url, timeout=3)
        status_code = response.status_code

        if response:
            result = response.json()

    except Exception:
        raise RequestException(status_code)

    return result
