from loguru import logger
from health_lifestyle_diabetes.domain.ports.logger_port import LoggerPort


class LoguruLogger(LoggerPort):
    """
    Adaptateur Loguru conforme au LoggerPort.

    - Ne configure pas Loguru (fait ailleurs, au point d'entrée).
    - Délègue les appels au logger global.
    - Remonte l'appelant réel grâce à `opt(depth=1)` pour
      afficher la bonne fonction, fichier et ligne dans les logs.
    """

    def info(self, message: str, **ctx) -> None:
        """Log une information décrivant le déroulement normal de l'application."""
        logger.bind(**ctx).opt(depth=1).info(message)

    def warning(self, message: str, **ctx) -> None:
        """Log un avertissement signalant une situation anormale non bloquante."""
        logger.bind(**ctx).opt(depth=1).warning(message)

    def error(self, message: str, **ctx) -> None:
        """Log une erreur indiquant un échec ou un comportement inattendu."""
        logger.bind(**ctx).opt(depth=1).error(message)

    def debug(self, message: str, **ctx) -> None:
        """Log un message de debug destiné au diagnostic technique."""
        logger.bind(**ctx).opt(depth=1).debug(message)