# src/health_lifestyle_diabetes/domain/ports/logger_port.py

from __future__ import annotations

from typing import Protocol


class LoggerPort(Protocol):
    """
    Port générique de logging pour respecter la Clean Architecture.

    Le domaine et l'application peuvent logguer sans connaître
    l'implémentation (loguru, stdlib logging, stackdriver, AWS, etc.).
    """

    def info(self, message: str) -> None: ...

    def warning(self, message: str) -> None: ...

    def error(self, message: str) -> None: ...

    def debug(self, message: str) -> None: ...
