"""
Port de journalisation destiné à isoler la couche application
des détails d'implémentation du logging (Loguru, standard logging, etc.).
"""

from typing import Protocol


class LoggerPort(Protocol):
    """Contrat minimal pour un service de journalisation."""

    def info(self, msg: str, *args, **kwargs) -> None:
        ...

    def warning(self, msg: str, *args, **kwargs) -> None:
        ...

    def error(self, msg: str, *args, **kwargs) -> None:
        ...

    def debug(self, msg: str, *args, **kwargs) -> None:
        ...
