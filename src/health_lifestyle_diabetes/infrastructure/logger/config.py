# src/health_lifestyle_diabetes/infrastructure/logger/config.py

import sys
from pathlib import Path

from loguru import logger

from health_lifestyle_diabetes.infrastructure.utils.paths import get_repository_root
from health_lifestyle_diabetes.infrastructure.utils.config_loader import YamlConfigLoader


def configure_logging(env: str = "dev") -> None:
    """
    Configure le logger global Loguru (console + fichier).

    Cette fonction :
    - configure les sinks Loguru,
    - s’applique au logger Loguru global (singleton),
    - doit être appelée UNE SEULE FOIS au point d’entrée de l’application.

    IMPORTANT :
    - Ne retourne rien.
    - Ne fournit pas d'instance de logger.
    - L'utilisation se fait via LoguruLogger (adaptateur).
    """

    # ── Load config (lazy, pas d'effet de bord à l'import)
    root = get_repository_root()
    cfg = YamlConfigLoader().load_config(root / "configs/paths.yaml")

    logs_dir = root / Path(cfg["logs"]["folder"])
    logs_dir.mkdir(parents=True, exist_ok=True)

    # ── Reset pour éviter les doublons (notebooks, reload, tests)
    logger.remove()

    # ─────────────────────────────────────────────────────────────
    # CONSOLE SINK (lisible humain, pour développement)
    # ─────────────────────────────────────────────────────────────
    logger.add(
        sys.stdout,
        level="DEBUG" if env == "dev" else "INFO",
        enqueue=True,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{file}:{line}</cyan> | "
            "<yellow>{function}()</yellow> | "
            "{message} | {extra}"
        ),
    )

    # ─────────────────────────────────────────────────────────────
    # FILE SINK (JSON structurel, prêt pour ELK/BigQuery/MLflow)
    # ─────────────────────────────────────────────────────────────
    logger.add(
        logs_dir / "health_lifestyle_diabetes.log",
        level="INFO",
        rotation="10 MB",
        retention="10 days",
        serialize=True,           # JSON pour ingestion machine
        backtrace=True,           # Stacktrace enrichie (utile prod)
        diagnose=False,           # N'affiche pas le contenu complet des objets (sécurité)
        enqueue=True,             # OK multiprocessing
    )

    logger.info("Loguru configuré avec succès (mode: {env})", env=env)