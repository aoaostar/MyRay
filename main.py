import asyncio
import os
from abc import ABC

from obj.base import Base
from obj.clash_chinese_patch import ClashChinesePatch
from obj.clash_for_windows_pkg import ClashForWindowsPkg
from obj.clash_meta import ClashMeta
from util import calculate_execution_time


@calculate_execution_time
async def task(clazz: (Base, ABC)):
    # filename: str
    # download_url: str
    #
    # filename, download_url = await clazz.get_download_url()
    # save_path = await clazz.download(download_url, filename)
    # clazz.extract(save_path, os.path.splitext(filename)[0])
    clazz.extract("./cache/Clash.for.Windows-0.20.28-win.7z","./cache/Clash.for.Windows-0.20.28-win")


@calculate_execution_time
async def main():
    result = await asyncio.gather(
        # task(ClashChinesePatch),
        task(ClashForWindowsPkg),
        # task(ClashMeta),
    )
    print("OK")


if __name__ == '__main__':
    asyncio.run(main())
