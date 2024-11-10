import vector_store_manager.config as config
import requests

def upload_file(filename: str, contents: bytes, content_type: str) -> str:
    """Загрузка файла на fileservice"""
    files = {"file": (filename, contents, content_type)}
    response = requests.post(f'{config.FILES_URL}/upload', files=files)
    if response.status_code == 200:
        data = response.json()
        return data["entries"][0]["id"]  # Возвращаем первую ссылку из массива paths
    else:
        raise Exception(f"Error fetching paths: {response.status_code} {response.json()}")  # Обработка ошибки