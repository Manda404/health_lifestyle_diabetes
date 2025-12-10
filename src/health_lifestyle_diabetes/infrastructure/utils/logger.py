# mypy: ignore-errors
"""
logger.py
---------

Système de logging centralisé basé sur Loguru.

Ce module fournit :
- Une configuration standardisée des logs (console + fichier)
- Rotation automatique des fichiers (20 MB)
- Rétention configurable (30 jours)
- Compression ZIP
- Support du binding (ajout de metadata : module, use-case, service…)
- Un accès unifié au logger pour tous les modules du projet

Pourquoi ce design ?
--------------------
Dans une architecture Clean, aucune couche (domain, application, infrastructure)
ne doit avoir à gérer la configuration du logging. Ce module sert donc
de point d’entrée unique, garantissant une structure cohérente et une
observabilité propre pour l’ensemble du projet.

Usage
-----
>>> from health_lifestyle_diabetes.infrastructure.utils.logger import get_logger
>>> logger = get_logger("training")
>>> logger.info("Démarrage de l'entraînement")
"""

import sys
from pathlib import Path

from health_lifestyle_diabetes.infrastructure.utils.paths import get_repository_root
from loguru import logger

# -------------------------------------------------------------------
# 1. Initialisation du dossier de logs
# -------------------------------------------------------------------
ROOT = get_repository_root()
DEFAULT_LOG_DIR = Path(ROOT / "logs")
DEFAULT_LOG_DIR.mkdir(exist_ok=True)


# -------------------------------------------------------------------
# 2. Fonction de configuration du logger global
# -------------------------------------------------------------------
def setup_logger(
    logger_name: str | None = None,
    *,
    log_name: str = "health_lifestyle_diabetes.log",
    level: str = "INFO",
):
    """
    Configure le logger global Loguru.

    Parameters
    ----------
    logger_name : str | None
        Nom associé au logger (souvent : module, service, use-case).
    log_name : str
        Nom du fichier log stocké dans le répertoire /logs/.
    level : str
        Niveau minimal du logging : DEBUG, INFO, WARNING, ERROR, CRITICAL.

    Returns
    -------
    logger : loguru.Logger
        Instance configurée du logger Loguru.
    """
    log_path = DEFAULT_LOG_DIR / log_name

    # Supprimer les handlers existants (console, fichiers…)
    logger.remove()

    # Ajouter metadata contextuelle (binding)
    bound_logger = logger.bind(logger_name=logger_name or "app")

    # ---------- Handler Console ----------
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

    # ---------- Handler Fichier ----------
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
# 3. Accès simplifié au logger
# -------------------------------------------------------------------
def get_logger(logger_name: str = "app"):
    """
    Récupère un logger configuré et prêt à l’emploi.

    Parameters
    ----------
    logger_name : str
        Nom du contexte d’utilisation (ex: "training", "api", "eda").

    Returns
    -------
    logger : loguru.Logger
        Logger préconfiguré pour ce module.
    """
    return setup_logger(logger_name=logger_name)
