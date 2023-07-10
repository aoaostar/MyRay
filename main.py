import asyncio
import os
import shutil
from abc import ABC

from logger import logger
from obj.base import Base
from obj.clash_chinese_patch import ClashChinesePatch
from obj.clash_for_windows_pkg import ClashForWindowsPkg
from obj.clash_meta import ClashMeta


async def task(clazz: (Base, ABC)):
    filename: str
    download_url: str

    filename, download_url = await clazz.get_download_url()
    save_path = await clazz.download(download_url, filename)
    extract_path = clazz.extract(save_path, os.path.splitext(filename)[0])
    return {
        "clazz": clazz,
        "save_path": save_path,
        "extract_path": extract_path,
    }


async def main():
    shutil.rmtree("./cache")
    pkg_latest_release = await Base.get_latest_release("Fndroid/clash_for_windows_pkg")
    my_ray_latest_release = await Base.get_latest_release("aoaostar/MyRay")
    if "tag_name" in my_ray_latest_release and pkg_latest_release["tag_name"] == my_ray_latest_release["tag_name"]:
        logger.info(
            f'当前已是最新版本, 当前版本: {my_ray_latest_release["tag_name"]} 最新版本: {pkg_latest_release["tag_name"]}')
        return
    result = await asyncio.gather(
        task(ClashChinesePatch),
        task(ClashForWindowsPkg),
        task(ClashMeta),
    )
    data = {}
    for r in result:
        data[r["clazz"]] = r

    merge_path = f'./cache/merge/{os.path.basename(data[ClashForWindowsPkg]["extract_path"])}'
    shutil.rmtree(merge_path)
    shutil.copytree(data[ClashForWindowsPkg]["extract_path"], merge_path)
    shutil.copy(data[ClashChinesePatch]["extract_path"] + "/app.asar", f"{merge_path}/resources/app.asar")
    shutil.copy(data[ClashMeta]["extract_path"] + "/clash.meta-windows-amd64.exe",
                f"{merge_path}/resources/static/files/win/x64/clash-win64.exe")
    shutil.make_archive(f"{merge_path}.zip", merge_path)


if __name__ == '__main__':
    asyncio.run(main())
