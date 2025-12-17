# src/health_lifestyle_diabetes/domain/services/threshold_service.py

"""
Service métier pour la gestion des seuils de décision.

Rôle :
------
- convertir des probabilités en labels binaires,
- centraliser la logique liée au seuil (facile à tester et modifier).
"""

from typing import List, Sequence


class ThresholdService:
    """
    Gère la conversion probabilité → label binaire via un seuil.
    """

    @staticmethod
    def apply_threshold(
        y_proba: Sequence[float],
        threshold: float,
    ) -> List[int]:
        """
        Convertit une séquence de probabilités en labels 0/1.

        Paramètres
        ----------
        y_proba : séquence de float
            Probabilités prédites pour la classe positive.
        threshold : float
            Seuil de décision (typiquement 0.5).

        Retour
        ------
        List[int]
            Labels binaires correspondant à la décision.
        """
        return [1 if p >= threshold else 0 for p in y_proba]
