import logging
import sys
from types import FrameType

import loguru

from app.settings import LoggingSettings


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        # Get corresponding Loguru level if it exists
        loglevel_mapping = {
            50: "CRITICAL",
            40: "ERROR",
            30: "WARNING",
            20: "INFO",
            10: "DEBUG",
            0: "NOTSET",
        }
        try:
            level: str | int = loguru.logger.level(record.levelname).name
        except ValueError:
            level = loglevel_mapping[record.levelno]

        # Find caller from where originated the logged message
        frame: FrameType | None
        frame, depth = logging.currentframe(), 2
        while frame is not None and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1
        loguru.logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def setup_logging(settings: LoggingSettings) -> None:
    # Setup logging
    logging.basicConfig(handlers=[InterceptHandler()], level=0)
    loguru_handlers = []

    format_ = (
        "<green>{time:YYYY-MM-DDTHH:mm:ss.SSS}</green> | <level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    )

    loguru_handlers += [
        {"sink": sys.stdout, "level": settings.level, "backtrace": False, "format": format_},
    ]

    loguru.logger.configure(handlers=loguru_handlers)
