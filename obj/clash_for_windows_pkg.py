import re
from abc import ABC

from obj.base import Base
from util import calculate_execution_time


class ClashForWindowsPkg(Base, ABC):

    @classmethod
    @calculate_execution_time
    async def get_download_url(cls):
        release = await cls.get_latest_release("Fndroid/clash_for_windows_pkg")
        for asset in release["assets"]:
            if re.match(r"^Clash\.for\.Windows-\d+\.\d+\.\d+-win\.7z$", asset["name"]):
                return asset["name"], asset["browser_download_url"]

    def aaa(self):
        pass