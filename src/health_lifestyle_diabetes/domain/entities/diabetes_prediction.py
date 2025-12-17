# src/health_lifestyle_diabetes/domain/entities/diabetes_prediction.py


"""
1. Sortie métier d'une prédiction effectuée par le modèle.

Cette entité encapsule :
- la probabilité prédite (ML → domaine)
- le label binaire déterminé via le seuil métier
- un niveau de risque interprétable
- le seuil utilisé (utile pour audit)

Elle permet de :
- rendre les résultats intelligibles pour utilisateurs métier / API / UI
- standardiser les réponses quel que soit le modèle ML derrière
- séparer le ML (infra) de l’interprétation (domaine)

2. Sortie métier d'une prédiction de diabète.

Cette entité encapsule le résultat interprété côté domaine :
- probabilité de diabète,
- label binaire (0/1),
- niveau de risque textuel,
- seuil utilisé lors de la décision.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class DiabetesPrediction:
    """
    Représentation d'une prédiction interprétée côté métier. (Résultat d'une prédiction de diabète interprétée pour le métier.)

    Cette entité encapsule :
    - la probabilité **prédite** par le modèle de classification (valeur brute ML),
    - la classe prédite **binaire** (0 ou 1) déterminée par l'application d'un seuil,
    - un niveau de risque **qualitatif** (e.g., "Faible", "Modéré", "Élevé", "Très Élevé") interprétable pour le métier,
    - le seuil **numérique** utilisé pour la détermination du label binaire (utile pour l'audit et la traçabilité).

    """

    probability: float
    predicted_label: int
    tag_label: str
    risk_level: str
    threshold_used: float
    explanation: Optional[str] = None
