"""
Entité métier regroupant les métriques d'évaluation d'un modèle de classification.

Elle sert de format de sortie standard :
- pour les use cases d'évaluation,
- pour les rapports,
- pour les dashboards.

MCC & Kappa :
-------------
Ce sont des métriques **techniques** utilisées surtout par les data scientists.
Elles ont **peu de valeur en décision clinique**, mais apportent une
information supplémentaire sur la robustesse du modèle (déséquilibre, accord).
"""

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass(frozen=True)
class EvaluationResults:
    """
    Résultats d'évaluation d'un modèle de classification binaire.
    """

    # Métriques principales
    auc_roc: Optional[float] = None
    auc_pr: Optional[float] = None
    accuracy: Optional[float] = None
    precision: Optional[float] = None
    recall: Optional[float] = None
    f1: Optional[float] = None

    # Taux d'erreurs issus de la matrice de confusion
    false_positive_rate: Optional[float] = None
    false_negative_rate: Optional[float] = None

    # Métriques avancées, plutôt techniques que cliniques
    kappa: Optional[float] = None  # technique, faible usage clinique direct
    mcc: Optional[float] = None  # technique, utile en cas de déséquilibre

    # Pour attacher toute autre métrique calculée par l'infrastructure
    extra_metrics: Optional[Dict[str, float]] = None
