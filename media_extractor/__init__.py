__version__ = '0.1.0'

import logging
import os

logging.basicConfig(
    level=os.environ.get("LOG_LEVEL") or logging.INFO,
    format="%(levelname)s\t%(asctime)s\t%(message)s",
)
