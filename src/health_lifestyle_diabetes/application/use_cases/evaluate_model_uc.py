# src/health_lifestyle_diabetes/application/use_cases/evaluate_model_uc.py

from typing import Sequence, Optional

from health_lifestyle_diabetes.domain.entities.evaluation_results import (
    EvaluationResults,
)
from health_lifestyle_diabetes.domain.ports.logger_port import LoggerPort
from health_lifestyle_diabetes.domain.ports.metrics_plotter_port import (
    MetricsPlotterPort,
)
from health_lifestyle_diabetes.domain.services.evaluation_service import (
    EvaluationService,
)


class EvaluateModelUseCase:
    """
    Use case d'évaluation d'un modèle de classification.

    Responsabilités :
    -----------------
    - orchestrer l'évaluation métier du modèle,
    - appliquer un seuil de décision,
    - produire un objet EvaluationResults normalisé,
    - déclencher optionnellement la visualisation des métriques.

    Règles Clean Architecture :
    ---------------------------
    - aucune dépendance vers infrastructure,
    - aucune dépendance vers sklearn / matplotlib / plotly,
    - uniquement domaine + ports abstraits.
    """

    def __init__(
        self,
        evaluation_service: EvaluationService,
        logger: LoggerPort,
        metrics_plotter: Optional[MetricsPlotterPort] = None,
    ):
        self.evaluation_service = evaluation_service
        self.logger = logger
        self.metrics_plotter = metrics_plotter

    # ------------------------------------------------------------------
    def execute(
        self,
        y_true: Sequence[int],
        y_proba: Sequence[float],
        *,
        threshold: float = 0.5,
        plot_metrics: bool = False,
        selected_metrics: Optional[Sequence[str]] = None,
        plot_title: str = "Model Evaluation Metrics",
    ) -> EvaluationResults:
        """
        Exécute l'évaluation complète du modèle.

        Parameters
        ----------
        y_true : sequence[int]
            Labels réels.
        y_proba : sequence[float]
            Probabilités prédites.
        plot_metrics : bool
            Active la visualisation.
        selected_metrics : sequence[str] | None
            Métriques à afficher.
        plot_title : str
            Titre du graphique.

        Returns
        -------
        EvaluationResults
            Résultats métier de l'évaluation.
        """

        self.logger.info("Démarrage de l'évaluation du modèle.")

        # 1. Évaluation métier
        results = self.evaluation_service.evaluate(
            y_true=y_true,
            y_proba=y_proba,
            threshold=threshold,
        )

        self.logger.info(
            f"Évaluation terminée | "
            f"AUC={results.auc_roc:.4f} | "
            f"F1={results.f1:.4f} | "
            f"Recall={results.recall:.4f}"
        )

        # 2. Visualisation optionnelle
        if plot_metrics:
            if not self.metrics_plotter:
                self.logger.warning(
                    "Visualisation demandée mais aucun MetricsPlotterPort injecté."
                )
            else:
                self.metrics_plotter.plot_metrics(
                    metrics=results.extra_metrics,
                    title=plot_title,
                    selected_metrics=selected_metrics,
                )

        self.logger.info("Use case EvaluateModelUseCase terminé.")

        return results