"""
Adaptateur de logger conforme au port `LoggerPort`.

Il encapsule le logger Loguru existant pour exposer uniquement les méthodes
utilisées depuis la couche application.
"""

from health_lifestyle_diabetes.domain.ports.logger_port import LoggerPort
from health_lifestyle_diabetes.infrastructure.utils.logger import get_logger


class LoggerAdapter(LoggerPort):
    def __init__(self, logger_name: str = "app") -> None:
        self._logger = get_logger(logger_name)

    def info(self, msg: str, *args, **kwargs) -> None:
        self._logger.info(msg, *args, **kwargs)

    def warning(self, msg: str, *args, **kwargs) -> None:
        self._logger.warning(msg, *args, **kwargs)

    def error(self, msg: str, *args, **kwargs) -> None:
        self._logger.error(msg, *args, **kwargs)

    def debug(self, msg: str, *args, **kwargs) -> None:
        self._logger.debug(msg, *args, **kwargs)
