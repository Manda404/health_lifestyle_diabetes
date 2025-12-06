import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from health_lifestyle_diabetes.infrastructure.utils.logger import get_logger
from health_lifestyle_diabetes.infrastructure.utils.paths import get_repository_root
from health_lifestyle_diabetes.infrastructure.utils.config_loader import ConfigLoader

logger = get_logger("evaluation.confusion_matrix")


class ConfusionMatrixPlotter:

    def __init__(self):
        """
        Paramètres internes : adaptés à ton projet diabète (binaire 0/1).
        """

        # Label technique des classes
        self.labels = [0, 1]

        # Labels affichés dans les axes
        self.class_labels = ["Non-Diabétique", "Diabétique"]

        # Paths YAML
        self.root = get_repository_root()
        self.paths = ConfigLoader.load_config(self.root / "configs/paths.yaml")

        logger.info("ConfusionMatrixPlotter initialized with default diabetes labels.")

    # ----------------------------
    # Internal static helpers
    # ----------------------------
    @staticmethod
    def __compute_confusion_matrices(y_true, y_pred, labels):
        cm = confusion_matrix(y_true, y_pred, labels=labels)

        row_sums = cm.sum(axis=1, keepdims=True)
        row_sums[row_sums == 0] = 1
        cmn = cm / row_sums * 100.0

        return cm, cmn

    @staticmethod
    def __plot_matrix(ax, y_true, y_pred, *, title, labels, class_labels, cmap):
        cm, cmn = ConfusionMatrixPlotter.__compute_confusion_matrices(
            y_true, y_pred, labels
        )

        im = ax.imshow(cmn, interpolation="nearest", cmap=cmap)

        ax.set_title(title, fontsize=14, fontweight="bold")
        ax.set_xlabel("Predicted label")
        ax.set_ylabel("True label")

        ax.set_xticks(range(len(labels)))
        ax.set_yticks(range(len(labels)))
        ax.set_xticklabels(class_labels)
        ax.set_yticklabels(class_labels)

        # values inside cells
        for i in range(len(labels)):
            for j in range(len(labels)):
                ax.text(
                    j, i, f"{cm[i,j]}\n({cmn[i,j]:.1f}%)",
                    ha="center", va="center",
                    fontsize=11,
                )

        plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

    # ----------------------------
    # Saving function
    # ----------------------------
    def __save_figure(self, fig, model_name: str) -> None:
        """
        Sauvegarde une figure matplotlib au format PNG 
        dans le dossier reports/cm_reports.
        """

        metric_name = "confusion_matrix"

        save_dir = Path(self.root / self.paths["reports"]["cm_reports"])
        save_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        png_path = save_dir / f"{timestamp}_{model_name.lower()}_{metric_name}.png"

        fig.savefig(png_path, format="png", dpi=300)

        logger.info(f"Confusion matrix saved at: {png_path}")

    # ==========================================================
    # PUBLIC ENTRY POINT
    # ==========================================================
    def plot_confusion_matrices(
        self,
        model,
        *,
        X_test,
        y_test,
        X_valid=None,
        y_valid=None,
        save_figure: bool = False,
        model_name: str = "model"
    ):
        """
        Affiche une ou deux matrices selon si un ensemble validation est fourni.
        Option : sauvegarder la figure générée.
        """

        logger.info("Generating confusion matrix plots...")

        y_pred_test = model.predict(X_test)
        y_pred_valid = model.predict(X_valid) if X_valid is not None else None

        # --- Cas 1 : seulement Test ---
        if X_valid is None or y_valid is None:
            fig, ax = plt.subplots(figsize=(7, 6))

            self.__plot_matrix(
                ax,
                y_true=y_test,
                y_pred=y_pred_test,
                title="Test — Confusion Matrix",
                labels=self.labels,
                class_labels=self.class_labels,
                cmap="Blues",
            )

            plt.tight_layout()
            plt.show()

            if save_figure:
                self.__save_figure(fig, model_name)

            return fig

        # --- Cas 2 : Test + Validation ---
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))

        # Validation
        self.__plot_matrix(
            axes[0],
            y_true=y_valid,
            y_pred=y_pred_valid,
            title="Validation — Confusion Matrix",
            labels=self.labels,
            class_labels=self.class_labels,
            cmap="Purples",
        )

        # Test
        self.__plot_matrix(
            axes[1],
            y_true=y_test,
            y_pred=y_pred_test,
            title="Test — Confusion Matrix",
            labels=self.labels,
            class_labels=self.class_labels,
            cmap="Blues",
        )

        plt.tight_layout()
        plt.show()

        if save_figure:
            self.__save_figure(fig, model_name)

        plt.close(fig)
