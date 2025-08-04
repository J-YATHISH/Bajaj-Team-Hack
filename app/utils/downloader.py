import requests
import tempfile

def download_file_from_url(url: str, suffix=".pdf") -> str:
    response = requests.get(url)
    response.raise_for_status()
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
        tmp_file.write(response.content)
        return tmp_file.name
