import requests
from requests import Response

def pageExist(url: str) -> tuple[Response, bool]:
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

    try:
        response = requests.get(url, headers=headers)
        return response, response.status_code // 100 == 2
    except requests.RequestException:
        return None, False
