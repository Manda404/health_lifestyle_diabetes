# src/health_lifestyle_diabetes/infrastructure/ml/evaluation/classification_evaluator.py

from dataclasses import dataclass
from typing import Any, List, Optional

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from health_lifestyle_diabetes.infrastructure.utils.logger import get_logger
from sklearn.metrics import (
    auc,
    average_precision_score,
    classification_report,
    confusion_matrix,
    precision_recall_curve,
    roc_curve,
)

from .probability_plotter import ProbabilityPlotter

logger = get_logger("evaluation.classification_evaluator")


@dataclass
class ClassificationEvaluator:
    """
    Orchestrateur d'évaluation pour un modèle de classification binaire.
    """

    model: Any
    X_test: np.ndarray
    y_test: np.ndarray
    class_names: Optional[List[str]] = None
    threshold: float = 0.5

    # ------------------------------------------------------------------
    def print_classification_metrics(self) -> None:
        logger.info("Calcul des métriques de classification…")
        probas = self.model.predict_proba(self.X_test)[:, 1]
        preds = (probas >= self.threshold).astype(int)

        logger.debug(f"Seuil utilisé : {self.threshold}")
        logger.debug(f"Distribution preds: {np.unique(preds, return_counts=True)}")

        report = classification_report(
            self.y_test,
            preds,
            target_names=self.class_names if self.class_names else None,
        )

        logger.info("=== Classification Report ===")
        logger.info(report)

        logger.info("Métriques de classification affichées.")

    # ------------------------------------------------------------------
    def plot_confusion_matrices(self) -> None:
        logger.info("Plot des matrices de confusion…")

        probas = self.model.predict_proba(self.X_test)[:, 1]
        preds = (probas >= self.threshold).astype(int)

        cm = confusion_matrix(self.y_test, preds)
        cm_norm = confusion_matrix(self.y_test, preds, normalize="true")

        logger.debug(f"Confusion matrix brute:\n{cm}")
        logger.debug(f"Confusion matrix normalisée:\n{cm_norm}")

        labels = self.class_names if self.class_names else ["Classe 0", "Classe 1"]

        fig, axes = plt.subplots(1, 2, figsize=(12, 5))

        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=axes[0])
        axes[0].set_title("Matrice de confusion (brute)")
        axes[0].set_xlabel("Prédit")
        axes[0].set_ylabel("Réel")
        axes[0].set_xticklabels(labels)
        axes[0].set_yticklabels(labels)

        sns.heatmap(cm_norm, annot=True, fmt=".2f", cmap="Blues", ax=axes[1])
        axes[1].set_title("Matrice de confusion (normalisée)")
        axes[1].set_xlabel("Prédit")
        axes[1].set_ylabel("Réel")
        axes[1].set_xticklabels(labels)
        axes[1].set_yticklabels(labels)

        plt.tight_layout()
        plt.show()

        logger.info("Matrice de confusion affichée.")

    # ------------------------------------------------------------------
    def plot_roc_curve(self) -> None:
        logger.info("Plot de la courbe ROC…")

        probas = self.model.predict_proba(self.X_test)[:, 1]
        fpr, tpr, _ = roc_curve(self.y_test, probas)
        roc_auc = auc(fpr, tpr)

        logger.debug(f"AUC = {roc_auc:.4f}")

        plt.figure(figsize=(7, 6))
        plt.plot(fpr, tpr, label=f"ROC curve (AUC = {roc_auc:.3f})")
        plt.plot([0, 1], [0, 1], "k--", label="Hasard")

        plt.title("Courbe ROC")
        plt.xlabel("FPR (Faux positifs)")
        plt.ylabel("TPR (Vrais positifs)")
        plt.legend()
        plt.grid(True, linestyle="--", alpha=0.3)
        plt.show()

        logger.info("Courbe ROC affichée.")

    # ------------------------------------------------------------------
    def plot_precision_recall_curve(self) -> None:
        logger.info("Plot de la courbe Precision-Recall…")

        probas = self.model.predict_proba(self.X_test)[:, 1]
        precision, recall, _ = precision_recall_curve(self.y_test, probas)
        ap = average_precision_score(self.y_test, probas)

        logger.debug(f"AP (Average Precision) = {ap:.4f}")

        plt.figure(figsize=(7, 6))
        plt.plot(recall, precision, label=f"PR curve (AP = {ap:.3f})")

        plt.title("Courbe Precision-Recall")
        plt.xlabel("Recall")
        plt.ylabel("Precision")
        plt.legend()
        plt.grid(True, linestyle="--", alpha=0.3)
        plt.show()

        logger.info("Courbe PR affichée.")

    # ------------------------------------------------------------------
    def plot_probability_analysis(self) -> None:
        logger.info("Analyse complète des probabilités — démarrage.")
        ProbabilityPlotter.plot_global_probability_distribution(self.model, self.X_test)
        ProbabilityPlotter.plot_probability_by_true_class(
            self.model, self.X_test, self.y_test
        )
        ProbabilityPlotter.plot_fp_fn_distribution(
            self.model, self.X_test, self.y_test, threshold=self.threshold
        )
        ProbabilityPlotter.plot_calibration_curve(self.model, self.X_test, self.y_test)
        ProbabilityPlotter.plot_threshold_view(
            self.model, self.X_test, threshold=self.threshold
        )
        logger.info("Analyse complète des probabilités — terminé.")

    # ------------------------------------------------------------------
    def run_full_evaluation(self) -> None:
        logger.info("Évaluation complète du modèle — démarrage.")
        self.print_classification_metrics()
        self.plot_confusion_matrices()
        self.plot_roc_curve()
        self.plot_precision_recall_curve()
        self.plot_probability_analysis()
        logger.info("Évaluation complète du modèle — terminé.")
