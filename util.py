import asyncio
import time

from logger import logger


def calculate_execution_time(func, title=None):
    async def wrapper_async(*args, **kwargs):
        nonlocal title
        start_time = time.time()
        result = await func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        if title is None:
            title = func.__name__
        logger.info(f"[{title}]耗费：{execution_time} seconds")
        return result

    def wrapper_sync(*args, **kwargs):
        nonlocal title
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        if title is None:
            title = func.__name__
        logger.info(f"[{title}]耗费：{execution_time} seconds")
        return result

    if asyncio.iscoroutinefunction(func):
        return wrapper_async
    else:
        return wrapper_sync
