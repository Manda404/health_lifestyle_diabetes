from datetime import datetime
from pathlib import Path
from typing import Optional
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix

from health_lifestyle_diabetes.infrastructure.utils.config_loader import YamlConfigLoader
from health_lifestyle_diabetes.domain.ports.logger_port import LoggerPort
from health_lifestyle_diabetes.infrastructure.utils.paths import get_repository_root
from health_lifestyle_diabetes.infrastructure.logger.loguru_logger import LoguruLogger


class ConfusionMatrixPlotter:

    def __init__(self, logger: Optional[LoggerPort] = None) -> None:
        """
        Classe dédiée à l'affichage et sauvegarde de matrices de confusion
        adaptées au domaine médical (diabète).
        Trois méthodes de normalisation disponibles :
        - row  (Recall) : éviter les faux négatifs (dépistage)
        - pred (Precision) DEFAULT : éviter les faux positifs (médecine)
        - diag (Analyse) : erreurs relatives / confusions clés
        """

        self.logger = logger or LoguruLogger()

        self.labels = [0, 1]
        self.class_labels = ["Non-Diabétique", "Diabétique"]

        self.root = get_repository_root()
        self.paths = YamlConfigLoader.load_config(f"{self.root}/configs/paths.yaml")

        self.logger.info("ConfusionMatrixPlotter initialized ⚕️ (default normalization : pred).")

    # ==========================================================
    # HELPERS : NORMALISATION
    # ==========================================================
    @staticmethod
    def __compute_confusion_matrix(y_true, y_pred, labels, method: str = "pred"):
        cm = confusion_matrix(y_true, y_pred, labels=labels).astype(float)

        if method == "row":  # Recall (éviter faux négatifs)
            row_sums = cm.sum(axis=1, keepdims=True)
            row_sums[row_sums == 0] = 1
            cm_norm = cm / row_sums * 100.0

        elif method == "pred":  # Precision (éviter faux positifs)
            col_sums = cm.sum(axis=0, keepdims=True)
            col_sums[col_sums == 0] = 1
            cm_norm = cm / col_sums * 100.0

        elif method == "diag":  # Analyse erreurs relatives
            diag_vals = np.diag(cm).reshape(-1, 1)
            diag_vals[diag_vals == 0] = 1
            cm_norm = cm / diag_vals * 100.0

        else:
            raise ValueError(
                f"Unknown normalization method '{method}'. Use: 'row' | 'pred' | 'diag'."
            )

        return cm, cm_norm


    # ==========================================================
    # HELPERS : DESCRIPTION MÉDICALE
    # ==========================================================
    def __get_normalization_description(self, method: str) -> str:
        descriptions = {
            "pred": "Précision : éviter les faux positifs (diagnostic erronné)",
            "row": "Recall : éviter les faux négatifs (rater un malade)",
            "diag": "Analyse : évaluer la gravité des confusions"
        }
        return descriptions.get(method, "Méthode inconnue")


    # ==========================================================
    # PLOT - MATRICE UNIQUE
    # ==========================================================
    @staticmethod
    def __plot_matrix(ax, y_true, y_pred, *, title, labels, class_labels, cmap, method):
        cm, cmn = ConfusionMatrixPlotter.__compute_confusion_matrix(
            y_true, y_pred, labels, method=method
        )

        im = ax.imshow(cmn, interpolation="nearest", cmap=cmap)
        ax.set_title(title, fontsize=14, fontweight="bold")
        ax.set_xlabel("Label Prédit")
        ax.set_ylabel("Label Réel")

        ax.set_xticks(range(len(labels)))
        ax.set_yticks(range(len(labels)))
        ax.set_xticklabels(class_labels)
        ax.set_yticklabels(class_labels)

        for i in range(len(labels)):
            for j in range(len(labels)):
                ax.text(
                    j, i,
                    f"{int(cm[i, j])}\n({cmn[i, j]:.1f}%)",
                    ha="center", va="center", fontsize=11
                )

        plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)


    # ==========================================================
    # SAVE TO PNG
    # ==========================================================
    def __save_figure(self, fig, run_name: str, method: str) -> None:
        save_dir = Path(self.root / self.paths["reports"]["cm_reports"])
        save_dir.mkdir(parents=True, exist_ok=True)

        file_name = f"{run_name}_confusion_matrix_{method}.png"
        path = save_dir / file_name

        fig.savefig(path, format="png", dpi=300)
        self.logger.info(f"Confusion matrix saved → {path}")


    # ==========================================================
    # PUBLIC : PLOT TEST + VALIDATION
    # ==========================================================
    def plot_confusion_matrices(
        self,
        model,
        *,
        X_test,
        y_test,
        X_valid=None,
        y_valid=None,
        normalization: str = "pred",
        save_figure: bool = False,
        run_name: str = "model_diabetes",
    ):

        desc = self.__get_normalization_description(normalization)
        self.logger.info(f"🩺 Normalisation sélectionnée → '{normalization}' ({desc})")

        y_pred_test = model.predict(X_test)
        y_pred_valid = model.predict(X_valid) if X_valid is not None else None


        # ------------------------------------------------------
        # Cas 1 : Seulement Test
        if X_valid is None or y_valid is None:
            fig, ax = plt.subplots(figsize=(7, 6))

            self.__plot_matrix(
                ax,
                y_true=y_test,
                y_pred=y_pred_test,
                title=f"TEST — méthode={normalization}",
                labels=self.labels,
                class_labels=self.class_labels,
                cmap="Blues",
                method=normalization,
            )

            # NOTE MÉDICALE EN-DESSOUS
            plt.figtext(
                0.5, -0.05,
                f"Note : {desc}",
                wrap=True, ha='center', fontsize=10, color="gray"
            )

            plt.tight_layout()
            plt.show()

            if save_figure:
                self.__save_figure(fig, run_name, normalization)

            return fig


        # ------------------------------------------------------
        # Cas 2 : Validation + Test
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))

        # VALIDATION
        self.__plot_matrix(
            axes[0], y_valid, y_pred_valid,
            title=f"VALIDATION — méthode={normalization}",
            labels=self.labels, class_labels=self.class_labels,
            cmap="Purples", method=normalization
        )

        # TEST
        self.__plot_matrix(
            axes[1], y_test, y_pred_test,
            title=f"TEST — méthode={normalization}",
            labels=self.labels, class_labels=self.class_labels,
            cmap="Blues", method=normalization
        )

        # NOTE MÉDICALE EN-DESSOUS
        plt.figtext(
            0.5, -0.05,
            f"Note : {desc}",
            wrap=True, ha='center', fontsize=10, color="gray"
        )

        plt.tight_layout()
        plt.show()

        if save_figure:
            self.__save_figure(fig, run_name, normalization)

        plt.close(fig)
