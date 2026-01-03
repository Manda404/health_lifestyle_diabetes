# src/health_lifestyle_diabetes/application/use_cases/evaluate_model_uc.py

from typing import Optional, Sequence

from health_lifestyle_diabetes.domain.entities.metrics import EvaluationResults
from health_lifestyle_diabetes.domain.ports.logger_port import LoggerPort
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
    ):
        self.evaluation_service = evaluation_service
        self.logger = logger



    # ------------------------------------------------------------------
    def execute(
        self,
        y_true: Sequence[int],
        y_proba: Sequence[float],
        *,
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

        # ------------------------------------------------------------------
        # Sanity checks / contexte
        # ------------------------------------------------------------------
        self.logger.debug(
            f"Input received | "
            f"n_samples={len(y_true)} | "
            f"plot_metrics={plot_metrics} | "
            f"selected_metrics={selected_metrics}"
        )

        # ------------------------------------------------------------------
        # Évaluation métier
        # ------------------------------------------------------------------
        self.logger.info("Lancement du service d'évaluation métier.")
        results = self.evaluation_service.evaluate(
            y_true=y_true,
            y_proba=y_proba,
        )

        self.logger.info(
            "Évaluation terminée | "
            f"AUC={results.auc_roc:.4f} | "
            f"F1={results.f1:.4f} | "
            f"Recall={results.recall:.4f} | "
            f"Precision={results.precision:.4f}"
        )

        self.logger.debug(
            f"Métriques supplémentaires disponibles : "
            f"{list(results.extra_metrics.keys()) if results.extra_metrics else 'Aucune'}"
        )

        # ------------------------------------------------------------------
        # Visualisation optionnelle
        # ------------------------------------------------------------------
        if plot_metrics:
            self.logger.info(
                "Visualisation des métriques activée | "
                f"title='{plot_title}'"
            )

            self.evaluation_service.plotter(
                metrics=results.extra_metrics or {},
                title=plot_title,
                selected_metrics=selected_metrics,
            )

            self.logger.info("Visualisation des métriques terminée.")
        else:
            self.logger.debug(
                "Visualisation désactivée (plot_metrics=False)."
            )

        self.logger.info("Use case EvaluateModelUseCase terminé avec succès.")

        return results
