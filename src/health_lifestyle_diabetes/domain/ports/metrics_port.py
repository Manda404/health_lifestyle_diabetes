"""
Port (interface) abstrait pour le calcul des métriques d'évaluation.

Objectif :
----------
Découpler complètement :
- la logique métier (domain)
- des outils techniques (sklearn, numpy, torch, etc.)

Ainsi, l'infrastructure pourra implémenter cette interface avec sklearn
ou toute autre librairie sans impacter le domaine.

Ce port est utilisé par :
- EvaluationService (qui orchestre l'évaluation)
"""

from typing import Dict, Protocol, Sequence


class MetricsPort(Protocol):
    """
    Interface définissant un service capable de calculer des métriques
    de classification à partir de y_true, y_pred et y_proba.

    L'infrastructure doit fournir une implémentation (ex: SklearnMetricsAdapter).
    """

    def compute_metrics(
        self,
        y_true: Sequence[int],
        y_pred: Sequence[int],
        y_proba: Sequence[float],
    ) -> Dict[str, float]:
        """
        Calcule un ensemble standard de métriques de classification.

        Paramètres
        ----------
        y_true : séquence d'entiers
            Labels réels (0/1).

        y_pred : séquence d'entiers
            Labels prédits après application du seuil (0/1).

        y_proba : séquence de flottants
            Probabilités prédites par le modèle.

        Retour
        ------
        dict
            Exemple :
            {
                "accuracy": 0.89,
                "precision": 0.91,
                "recall": 0.78,
                "f1": 0.84,
                "auc_roc": 0.92,
                "auc_pr": 0.88,
                "kappa": 0.61,
                ...
            }

        Notes
        -----
        - Le domaine n'a aucune dépendance vers sklearn.
        - MCC peut être calculé dans l'infrastructure ou dans le domaine.
        """
        ...
