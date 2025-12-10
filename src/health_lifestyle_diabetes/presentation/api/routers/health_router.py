# src/health_lifestyle_diabetes/presentation/api/routers/health_router.py

from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/health")
def health_check() -> dict:
    """
    Endpoint de health-check minimal.

    Permet de vérifier rapidement que l'API est démarrée et répond.
    Utilisé par :
    - les load balancers
    - les probes Kubernetes
    - les tests de monitoring

    Retourne un simple JSON indiquant le statut.
    """
    return {"status": "ok", "message": "API is up and running."}
