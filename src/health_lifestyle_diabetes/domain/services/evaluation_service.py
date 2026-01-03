from typing import Sequence

from health_lifestyle_diabetes.domain.entities.decision_threshold_policy import (
    DecisionThresholdPolicy,
)
from health_lifestyle_diabetes.domain.entities.metrics import EvaluationResults
from health_lifestyle_diabetes.domain.ports.metrics_port import MetricsPort
from health_lifestyle_diabetes.domain.services.threshold_service import ThresholdService
from health_lifestyle_diabetes.domain.ports.metrics_plotter_port import (
    MetricsPlotterPort,
)

from typing import Optional, Dict

class EvaluationService:
    """
    Service applicatif orchestrant l'évaluation d'un modèle.
    """

    def __init__(self, metrics_adapter: MetricsPort, decision_threshold: DecisionThresholdPolicy, plotter: MetricsPlotterPort):
        self.metrics_adapter = metrics_adapter
        self.decision_threshold = decision_threshold
        self.metrics_plotter = plotter


    def evaluate(
        self,
        y_true: Sequence[int],
        y_proba: Sequence[float],
    ) -> EvaluationResults:
        # Application directe du seuil métier pour assurer une décision stable et cohérente.
        y_pred = ThresholdService.apply_threshold(y_proba, threshold=self.decision_threshold.threshold)
        metrics = self.metrics_adapter.compute_metrics(y_true, y_pred, y_proba)

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

    def plotter(self,
                metrics: Dict[str, float],
                *,
                title: str,
                selected_metrics: Optional[Sequence[str]] = None,
                ) -> None:
        self.metrics_plotter.plot_metrics(
            metrics=metrics,
            title=title,
            selected_metrics=selected_metrics,
            )
