from typing import Dict, Sequence

from health_lifestyle_diabetes.domain.ports.metrics_port import MetricsPort
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    cohen_kappa_score,
    confusion_matrix,
    f1_score,
    matthews_corrcoef,
    precision_score,
    recall_score,
    roc_auc_score,
)


class SklearnMetricsAdapter(MetricsPort):
    """Implémentation technique du calcul des métriques (avec sécurité & arrondi)."""

    @staticmethod
    def safe_division(numerator: float, denominator: float) -> float:
        """Retourne numerator/denominator, ou 0 si impossible (division par zéro)."""
        return 0.0 if denominator == 0 else numerator / denominator

    @staticmethod
    def r(value: float) -> float:
        """Arrondit à 4 décimales."""
        return round(value, 4)

    def compute_metrics(
        self,
        y_true: Sequence[int],
        y_pred: Sequence[int],
        y_proba: Sequence[float],
    ) -> Dict[str, float]:

        tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()

        # Calculs sécurisés
        fpr = self.safe_division(fp, fp + tn)
        fnr = self.safe_division(fn, fn + tp)

        mcc = (
            matthews_corrcoef(y_true, y_pred)
            if len(set(y_pred)) > 1 else 0.0
        )

        # Retour arrondi à 4 décimales
        return {
            "accuracy": self.r(accuracy_score(y_true, y_pred)),
            "precision": self.r(precision_score(y_true, y_pred, zero_division=0)),
            "recall": self.r(recall_score(y_true, y_pred, zero_division=0)),
            "f1": self.r(f1_score(y_true, y_pred, zero_division=0)),

            "auc_roc": self.r(roc_auc_score(y_true, y_proba)),
            "auc_pr": self.r(average_precision_score(y_true, y_proba)),

            "false_positive_rate": self.r(fpr),
            "false_negative_rate": self.r(fnr),

            "kappa": self.r(cohen_kappa_score(y_true, y_pred)),
            "mcc": self.r(mcc),
        }
