import re
from abc import ABC

from obj.base import Base
from util import calculate_execution_time


class ClashMeta(Base, ABC):

    @classmethod
    @calculate_execution_time
    async def get_download_url(cls):
        release = await cls.get_latest_release("MetaCubeX/Clash.Meta")
        for asset in release["assets"]:
            if re.match(r"^clash\.meta-windows-amd64-v\d+\.\d+\.\d+\.zip$", asset["name"]):
                return asset["name"], asset["browser_download_url"]
