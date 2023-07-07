from abc import ABC

from obj.base import Base
from util import calculate_execution_time


class ClashChinesePatch(Base, ABC):

    @classmethod
    @calculate_execution_time
    async def get_download_url(cls):
        release = await cls.get_latest_release("BoyceLig/Clash_Chinese_Patch")
        for asset in release["assets"]:
            if asset["name"] == "app.7z":
                return asset["name"], asset["browser_download_url"]
