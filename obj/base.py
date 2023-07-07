import os.path
from abc import abstractmethod

import httpx

from logger import logger
from util import calculate_execution_time


class Base:
    cache = "./cache"

    @classmethod
    @calculate_execution_time
    async def get_latest_release(cls, repo: str):
        url = f"https://api.github.com/repos/{repo}/releases/latest"
        async with httpx.AsyncClient() as client:
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
            os.makedirs(os.path.dirname(save_path), 777)

        async with httpx.AsyncClient() as client:
            async with client.stream("GET", "https://ghproxy.com/" + url, follow_redirects=True) as response:
                with open(save_path, "wb") as f:
                    async for chunk in response.aiter_bytes():
                        f.write(chunk)

        return save_path

    @classmethod
    @calculate_execution_time
    def extract(cls, archive_path: str, extract_path: str):
        extract_path = f"{cls.cache}/{extract_path}"
        logger.info(f"[{cls.__name__}][extract] archive_path={archive_path} extract_path={extract_path}")
        if not os.path.isdir(extract_path):
            os.makedirs(extract_path, 777)
        if "zip" in os.path.splitext(archive_path)[1]:
            import shutil
            shutil.unpack_archive(archive_path, extract_path)
        elif "7z" in os.path.splitext(archive_path)[1]:
            # import py7zr
            # with py7zr.SevenZipFile(archive_path, mode="r") as z:
            #     z.extractall(path=extract_path)
            from pyunpack import Archive

            Archive(archive_path).extractall(extract_path)

    @abstractmethod
    @calculate_execution_time
    async def get_download_url(self) -> tuple[str, str]:
        pass
