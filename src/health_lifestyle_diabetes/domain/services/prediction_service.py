# src/health_lifestyle_diabetes/domain/services/prediction_service.py
"""
Service métier de prédiction.

Rôle :
------
- demander au modèle ML une probabilité
- appliquer un seuil métier
- générer un objet DiabetesPrediction interprétable
- définir un niveau de risque basé sur la probabilité

Contraintes :
-------------
- aucune dépendance technique (pandas, sklearn, CatBoost, etc.)
- uniquement du métier

Le modèle est typé de manière "duck-typed" :
il doit exposer :
    predict_proba(patient: PatientProfile) -> float
"""

from dataclasses import dataclass
from typing import Protocol

from ..entities.diabetes_prediction import DiabetesPrediction
from ..entities.patient_profile import PatientProfile


class _SupportsPredictProba(Protocol):
    """
    Protocole interne décrivant ce que le service attend du modèle de prédiction.
    """

    def predict_proba(self, patient: PatientProfile) -> float: ...


@dataclass
class PredictionService:
    """
    Service d'orchestration métier autour de la prédiction patient.
    """

    model: _SupportsPredictProba
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
        """
        prob = self.model.predict_proba(patient)
        label = int(prob >= self.threshold)

        return DiabetesPrediction(
            probability=prob,
            predicted_label=label,
            risk_level=self._risk_level(prob),
            threshold_used=self.threshold,
        )
