import os.path
import subprocess
from abc import abstractmethod

import httpx

from logger import logger
from util import calculate_execution_time


def async_client():
    return httpx.AsyncClient(transport=httpx.AsyncHTTPTransport(retries=3))


class Base:
    cache = "./cache"
    # proxy = "https://ghproxy.com/"
    proxy = ""

    @classmethod
    @calculate_execution_time
    async def get_latest_release(cls, repo: str):
        url = f"https://api.github.com/repos/{repo}/releases/latest"
        async with async_client() as client:
            response = await client.get(url)
            response_json = response.json()
            if "message" in response_json:
                logger.error(
                    f"[{cls.__name__}][get_latest_release] message={response_json['message']}", )
            return response_json

    @classmethod
    @calculate_execution_time
    async def download(cls, url: str, filename: str):
        save_path = f"{cls.cache}/{filename}"
        if not os.path.exists(os.path.dirname(save_path)):
            os.makedirs(os.path.dirname(save_path))

        logger.info("save_path " + save_path)

        async with async_client() as client:
            async with client.stream("GET", cls.proxy + url, follow_redirects=True) as response:
                with open(save_path, "wb") as f:
                    async for chunk in response.aiter_bytes():
                        f.write(chunk)

        return save_path

    @classmethod
    @calculate_execution_time
    def extract(cls, archive_path: str, extract_path: str):
        extract_path = f"{cls.cache}/{extract_path}"
        if not os.path.exists(extract_path):
            os.makedirs(extract_path)
        subprocess.run(f'''7z x "{archive_path}" -o"{extract_path}" -bsp1 -bso0''')
        return extract_path

    @abstractmethod
    async def get_download_url(self) -> tuple[str, str]:
        pass
