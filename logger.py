import logging

logging.basicConfig(
    level=logging.INFO,
    format="[%(name)s][%(levelname)s][%(asctime)s] %(message)s",
)
logger = logging.getLogger("MyRay")
