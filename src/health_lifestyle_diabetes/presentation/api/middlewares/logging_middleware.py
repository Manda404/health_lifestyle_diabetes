# src/health_lifestyle_diabetes/presentation/api/middlewares/logging_middleware.py

import time

from fastapi import FastAPI, Request
from health_lifestyle_diabetes.infrastructure.utils.logger import get_logger

logger = get_logger("api.middleware FastAPI")


def add_logging_middleware(app: FastAPI) -> None:
    """
    Ajoute un middleware FastAPI pour logger chaque requête HTTP.

    Ce middleware :
    - mesure le temps de traitement de chaque requête
    - loggue la méthode HTTP, le chemin et la durée
    - ajoute un header `X-Response-Time` dans la réponse

    Avantages :
    - visibilité sur les performances
    - utile pour le debug et le monitoring
    """

    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start = time.time()

        response = await call_next(request)

        duration_ms = (time.time() - start) * 1000
        logger.info(f"{request.method} {request.url.path} — {duration_ms:.2f} ms")

        # Ajoute un header technique pour le suivi des temps de réponse
        response.headers["X-Response-Time"] = f"{duration_ms:.2f}ms"
        return response
