# src/health_lifestyle_diabetes/presentation/api/config/cors.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def add_cors(app: FastAPI) -> None:
    """
    Configure la politique CORS de l'API.

    CORS (Cross-Origin Resource Sharing) contrôle quels domaines
    ont le droit d'appeler l'API depuis un navigateur (JavaScript).

    Pour le développement, on autorise tout (`*`), mais en production,
    il est recommandé de restreindre à une liste de domaines connus.
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "*"
        ],  # TODO: restreindre en prod (ex: ["https://mon-front.com"])
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
