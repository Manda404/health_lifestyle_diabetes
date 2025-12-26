# src/health_lifestyle_diabetes/domain/ports/logger_port.py

from __future__ import annotations
from typing import Protocol


class LoggerPort(Protocol):
    """
    Port générique de logging pour respecter la Clean Architecture.

    Le domaine et l'application peuvent émettre des logs sans connaître
    l'implémentation concrète (stdlib logging, loguru, cloud logging, etc.).
    """

    def debug(self, message: str) -> None:
        """
        Log un message de debug destiné au diagnostic technique.
        """
        ...

    def info(self, message: str) -> None:
        """
        Log une information décrivant le déroulement normal de l'application.
        """
        ...

    def warning(self, message: str) -> None:
        """
        Log un avertissement signalant une situation anormale mais non bloquante.
        """
        ...

    def error(self, message: str) -> None:
        """
        Log une erreur indiquant un échec ou un comportement inattendu.
        """
        ...