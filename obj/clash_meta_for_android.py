from abc import ABC

from obj.base import Base
from util import calculate_execution_time


class ClashMetaForAndroid(Base, ABC):

    @classmethod
    @calculate_execution_time
    async def get_download_url(cls):
        release = await cls.get_latest_release("MetaCubeX/ClashMetaForAndroid")
        for asset in release["assets"]:
            if asset["name"].__contains__("meta-arm64-v8a-release.apk"):
                return asset["name"], asset["browser_download_url"]

    @classmethod
    @calculate_execution_time
    def extract(cls, archive_path: str, extract_path: str):
        return archive_path
