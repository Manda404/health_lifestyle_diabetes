"""
logger.py
---------

Système de logging basé sur Loguru, adapté à une architecture Clean.

Fonctionnalités :
- Logging console + fichier
- Rotation automatique
- Rétention configurable
- Compression ZIP
- Support du binding (ex: module_name)
- Compatible avec tous les modules du projet

Usage :

from health_lifestyle_diabetes.infrastructure.utils.logger import setup_logger, get_logger

logger = get_logger("training")
logger.info("Training started.")
"""

import sys
from pathlib import Path
from loguru import logger
from health_lifestyle_diabetes.infrastructure.utils.paths import get_repository_root


# -------------------------------------------------------------------
# 1. Dossier de logs (créé automatiquement si absent)
# -------------------------------------------------------------------
ROOT = get_repository_root()
DEFAULT_LOG_DIR = Path(ROOT / "logs")
DEFAULT_LOG_DIR.mkdir(exist_ok=True)


# -------------------------------------------------------------------
# 2. Fonction de configuration globale du logger
# -------------------------------------------------------------------
def setup_logger(
    logger_name: str | None = None,
    *,
    log_name: str = "health_lifestyle_diabetes.log",
    level: str = "INFO",
) -> "logger":
    """
    Configure le logger global avec Loguru.

    Parameters
    ----------
    logger_name : str | None
        Nom du logger (affiché dans les logs via extra metadata).
    log_name : str
        Nom du fichier de log.
    level : str
        Niveau minimal : DEBUG, INFO, WARNING, ERROR, CRITICAL.

    Returns
    -------
    logger : loguru.Logger
        Le logger configuré.
    """
    log_path = DEFAULT_LOG_DIR / log_name

    # -----------------------------
    # Supprimer tous les handlers existants
    # -----------------------------
    logger.remove()

    # -----------------------------
    # Ajouter metadata (module, use-case, etc.)
    # -----------------------------
    bound_logger = logger.bind(logger_name=logger_name or "app")

    # -----------------------------
    # Handler Console
    # -----------------------------
    bound_logger.add(
        sys.stdout,
        level=level.upper(),
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level:<8}</level> | "
            "<magenta>{extra[logger_name]}</magenta> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
            "<level>{message}</level>"
        ),
    )

    # -----------------------------
    # Handler Fichier
    # -----------------------------
    bound_logger.add(
        str(log_path),
        rotation="20 MB",
        retention="30 days",
        compression="zip",
        level=level.upper(),
        format=(
            "{time:YYYY-MM-DD HH:mm:ss} | "
            "{level:<8} | "
            "{extra[logger_name]} | "
            "{name}:{function}:{line} - {message}"
        ),
    )

    return bound_logger


# -------------------------------------------------------------------
# 3. Raccourci pratique : récupérer un logger configuré
# -------------------------------------------------------------------
def get_logger(logger_name: str = "app"):
    """
    Récupère un logger configuré. Idéal pour tous les modules du projet.

    Exemple :
    >>> logger = get_logger("training")
    >>> logger.info("start training")

    """
    return setup_logger(logger_name=logger_name)
