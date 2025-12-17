# src/health_lifestyle_diabetes/infrastructure/logging/logger_adapter.py
"""
Adaptateur Loguru conforme au LoggerPort.
C'est LA SEULE façon dont le reste de l'application doit accéder à Loguru.
"""
from __future__ import annotations

from health_lifestyle_diabetes.domain.ports.logger_port import LoggerPort
from health_lifestyle_diabetes.infrastructure.utils.logger import get_logger


class LoguruLoggerAdapter(LoggerPort):
    """
    Adaptateur Clean Architecture pour utiliser Loguru
    à travers le port LoggerPort.
    """

    def __init__(self, logger_name: str = "app") -> None:
        """
        Parameters
        ----------
        logger_name : str
            Nom logique du logger (module, use-case, contexte…)
        """
        self._logger = get_logger(logger_name)

    def info(self, message: str) -> None:
        self._logger.info(message)

    def warning(self, message: str) -> None:
        self._logger.warning(message)

    def error(self, message: str) -> None:
        self._logger.error(message)

    def debug(self, message: str) -> None:
        self._logger.debug(message)
