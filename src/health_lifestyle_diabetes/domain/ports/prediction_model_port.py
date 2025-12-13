"""
Port abstrait pour tout modèle de prédiction binaire.

Objectifs :
-----------
- Découpler complètement le domaine de l'infrastructure ML.
- Permettre de substituer CatBoost, XGBoost, RandomForest ou un modèle deep learning
  sans modifier la logique métier.
- Rendre testable le domaine via des mocks.

Ce port définit le comportement minimal d'un modèle utilisable par le domaine.
"""

from typing import Protocol

from ..entities.patient_profile import PatientProfile


class PredictionModelPort(Protocol):
    """
    Interface d'un modèle de prédiction binaire.
    """

    def predict_proba(self, patient: PatientProfile) -> float:
        """
        Retourne une probabilité de risque de diabète pour un patient.

        Paramètres
        ----------
        patient : PatientProfile
            Entité métier représentant un individu.

        Retour
        ------
        float : probabilité de diabète (entre 0 et 1)
        """
        ...
