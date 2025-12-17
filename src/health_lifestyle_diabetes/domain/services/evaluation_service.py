"""
Service métier d’évaluation globale du modèle de classification.

Rôle :
------
- appliquer un seuil pour transformer les probabilités en labels,
- calculer la matrice de confusion (TN, FP, FN, TP),
- calculer MCC dans le domaine,
- déléguer le calcul des métriques (AUC, F1, Kappa, etc.) au MetricsPort,
- produire un objet EvaluationResults normalisé.

Remarque :
----------
- MCC et Kappa sont des métriques techniques peu utilisées en décision clinique,
  mais utiles pour une analyse fine du modèle.
"""

from dataclasses import dataclass
from typing import Sequence

from ..entities.evaluation_results import EvaluationResults
from ..ports.metrics_port import MetricsPort
from .threshold_service import ThresholdService


@dataclass
class EvaluationService:
    """
    Orchestrateur métier pour l'évaluation de modèle.
    """

    metrics_port: MetricsPort
    threshold: float = 0.5

    def evaluate(
        self,
        y_true: Sequence[int],
        y_proba: Sequence[float],
    ) -> EvaluationResults:
        """
        Évalue un modèle à partir des labels réels et des probabilités prédites.

        Paramètres
        ----------
        y_true : séquence d'int
            Labels réels (0 ou 1).
        y_proba : séquence de float
            Probabilités prédites (entre 0 et 1).

        Retour
        ------
        EvaluationResults
            Objet métier regroupant toutes les métriques utiles.
        """

        # 1. Règle métier : Application du seuil → labels prédits 
        y_pred = ThresholdService.apply_threshold(y_proba, self.threshold)

        #2. Calcul technique (infra)
        metrics = self.metrics_port.compute_metrics(
            y_true=y_true,
            y_pred=y_pred,
            y_proba=y_proba,
        )

        #3. Normalisation métier
        return EvaluationResults(
            auc_roc=metrics.get("auc_roc"),
            auc_pr=metrics.get("auc_pr"),
            accuracy=metrics.get("accuracy"),
            precision=metrics.get("precision"),
            recall=metrics.get("recall"),
            f1=metrics.get("f1"),
            false_positive_rate=metrics.get("fpr"),
            false_negative_rate=metrics.get("fnr"),
            kappa=metrics.get("kappa"),
            mcc=metrics.get("mcc"),
            extra_metrics=metrics,
        )
