"""
Service métier de prédiction.

Rôle :
------
- demander au modèle une probabilité de diabète,
- appliquer la logique de seuil,
- produire un objet DiabetesPrediction interprétable pour le métier.

Le modèle est typé de manière "duck-typed" :
il doit simplement exposer une méthode `predict_proba(patient: PatientProfile) -> float`.
"""

from dataclasses import dataclass
from typing import Any, Optional

from ..entities.patient_profile import PatientProfile
from ..entities.diabetes_prediction import DiabetesPrediction



@dataclass
class PredictionService:
    """
    Service d'orchestration métier autour de la prédiction patient.
    """

    model: Optional[Any] = None
    threshold: float = 0.5

    def _risk_level(self, p: float) -> str:
        """
        Convertit une probabilité en niveau de risque textuel.
        """
        if p < 0.20:
            return "Faible"
        if p < 0.50:
            return "Modéré"
        if p < 0.80:
            return "Élevé"
        return "Très élevé"

    def predict(self, patient: PatientProfile) -> DiabetesPrediction:
        """
        Produit une prédiction interprétée pour un patient donné.

        Étapes :
        --------
        1. Probabilité brute via le modèle.
        2. Application du seuil pour le label.
        3. Détermination du niveau de risque.
        4. Construction de l'entité DiabetesPrediction.
        """
        prob = self.model.predict_proba(patient)
        label = int(prob >= self.threshold)
        tag_label = "Diabetic" if prob >= self.threshold else "Non-Diabetic"
        risk_level = self._risk_level(prob)
        return DiabetesPrediction(
            probability=prob,
            predicted_label=label,
            tag_label = tag_label,
            risk_level=risk_level,
            threshold_used=self.threshold,
            explanation = (
            f"Probabilité estimée de diabète = {prob:.2%}, "
            f"niveau de risque : {risk_level}."
            ),
        )