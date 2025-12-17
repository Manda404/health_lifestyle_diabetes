# src/health_lifestyle_diabetes/presentation/api/fastapi_app.py

from fastapi import FastAPI

from health_lifestyle_diabetes.infrastructure.utils.logger import get_logger
from health_lifestyle_diabetes.presentation.api.config.cors import add_cors
from health_lifestyle_diabetes.presentation.api.middlewares.logging_middleware import (
    add_logging_middleware,
)
from health_lifestyle_diabetes.presentation.api.routers.health_router import (
    router as health_router,
)


def create_app() -> FastAPI:
    """
    Crée et configure l'application FastAPI.

    Cette fonction est le point central de construction de l'API :
    - instanciation de FastAPI
    - ajout des middlewares (logs, CORS, etc.)
    - enregistrement des routers (health, predict, train, ...)

    Le fait de passer par une fonction `create_app` permet :
    - de tester plus facilement (on peut créer une app en test)
    - de configurer différemment l'app selon l'environnement (dev, prod, test)
    """
    app = FastAPI(
        title="Health Lifestyle Diabetes API",
        version="1.0.0",
        description="API REST pour la prédiction du diabète et l'analyse des profils santé.",
    )

    # initialisation du logger
    logger = get_logger("api.application FastAPI")

    # Ajout des middlewares transverses (logs, temps de réponse, etc.)
    add_logging_middleware(app)

    # Configuration CORS (qui a le droit d'appeler l'API)
    add_cors(app)

    # Enregistrement des routers
    app.include_router(health_router, prefix="/v1")

    logger.info("FastAPI application initialisée.")

    return app


# Instance globale de l'application utilisée par Uvicorn / Gunicorn
app = create_app()
