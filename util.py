import asyncio
import time

from logger import logger


def calculate_execution_time(func, title=None):
    if title is not None:
        title = f"[{title.__name__}][{func.__name__}]"
    else:
        title = f"[{func.__name__}]"

    if asyncio.iscoroutinefunction(func):
        # 处理异步方法
        async def wrapper(cls_, *args, **kwargs):
            nonlocal title
            start_time = time.time()
            result = await func(cls_, *args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time
            logger.info(f"{title} 耗费：{execution_time} seconds")
            return result

    else:
        # 处理同步方法
        def wrapper(cls_, *args, **kwargs):
            nonlocal title
            start_time = time.time()
            result = func(cls_, *args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time
            logger.info(f"{title} 耗费：{execution_time} seconds")
            return result

    return wrapper
