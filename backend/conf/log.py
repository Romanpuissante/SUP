import sys
from pathlib import Path
from loguru import logger

BASE_LOG = Path(__file__).parent.parent.joinpath("logs")

logger.level("TRASH", no=38, color="<blue>")
logger.add(BASE_LOG.joinpath("errors.log"), level="ERROR", backtrace=True, diagnose=True, rotation="1 week", compression="zip")
