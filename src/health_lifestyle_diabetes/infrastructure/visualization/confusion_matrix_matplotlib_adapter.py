from pathlib import Path
from typing import Any, Optional
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import confusion_matrix

from health_lifestyle_diabetes.domain.ports.confusion_matrix_plot_port import ConfusionMatrixPlotPort
from health_lifestyle_diabetes.domain.entities.confusion_matrix_config import ConfusionMatrixConfig
from health_lifestyle_diabetes.domain.ports.logger_port import LoggerPort
from health_lifestyle_diabetes.infrastructure.utils.config_loader import YamlConfigLoader
from health_lifestyle_diabetes.infrastructure.utils.paths import get_repository_root


class ConfusionMatrixMatplotlibAdapter(ConfusionMatrixPlotPort):
    """
    Implémentation Matplotlib pour afficher et/ou sauvegarder
    des matrices de confusion (une ou deux).
    """

    def __init__(self, logger: LoggerPort):
        self.logger = logger

        root = get_repository_root()
        cfg = YamlConfigLoader.load_config(f"{root}/configs/paths.yaml")
        self.save_dir = Path(root / cfg["reports"]["cm_reports"])
        self.save_dir.mkdir(parents=True, exist_ok=True)


    # ---------------------------------------------------------------------
    # Description textuelle selon normalisation (affichée sous la figure)
    # ---------------------------------------------------------------------
    def _get_normalization_description(self, method: str) -> str:
        desc = {
            "pred": "Normalisation par colonnes (précision, réduction des faux positifs).",
            "row":  "Normalisation par lignes (recall, réduction des faux négatifs).",
            "diag": "Normalisation sur la diagonale (analyse des confusions relatives).",
        }
        return desc.get(method, "Méthode de normalisation inconnue.")


    # ---------------------------------------------------------------------
    # Méthode appelée par le service (port)
    # ---------------------------------------------------------------------
    def plot(
        self,
        model: Any,
        *,
        X_test: Any,
        y_test: Any,
        config: ConfusionMatrixConfig,
        X_valid: Optional[Any] = None,
        y_valid: Optional[Any] = None,
        run_name: Optional[str] = None,
        save: bool = False
    ) -> None:

        self.logger.info(f"[ADAPTER] CM | normalization={config.normalization}")

        y_pred_test = self._predict(model, X_test)
        y_pred_valid = self._predict(model, X_valid) if X_valid is not None else None

        if X_valid is None or y_valid is None:
            fig = self._plot_single(y_test, y_pred_test, config)
        else:
            fig = self._plot_dual(y_test, y_pred_test, y_valid, y_pred_valid, config)

        if save:
            file = self.save_dir / f"{run_name}_cm_{config.normalization}.png"
            fig.savefig(file, dpi=300)
            self.logger.info(f"[ADAPTER] Sauvegardé -> {file}")

        plt.close(fig)


    # ---------------------------------------------------------------------
    # Helpers internes
    # ---------------------------------------------------------------------
    def _predict(self, model, X):
        """Transforme automatiquement les probabilités en classes si besoin."""
        if X is None:
            return None
        y = model.predict(X)
        if isinstance(y[0], float):  # prédictions = probabilités
            y = (y > 0.5).astype(int)
        return y

    def _normalize(self, cm, method):
        """Normalisation par 'pred' | 'row' | 'diag'."""
        if method == "row":
            s = cm.sum(axis=1, keepdims=True)
        elif method == "pred":
            s = cm.sum(axis=0, keepdims=True)
        elif method == "diag":
            s = np.diag(cm).reshape(-1, 1).astype(float).copy()  # FIX → copy()
        else:
            raise ValueError("Normalisation non reconnue.")
        s[s == 0] = 1
        return (cm / s) * 100


    # ---------------------------------------------------------------------
    # Plot de base (appelé par single / dual)
    # ---------------------------------------------------------------------
    def _plot_matrix(self, ax, y_true, y_pred, title, config, cmap):

        labels = config.labels
        class_labels = config.class_labels
        method = config.normalization

        cm = confusion_matrix(y_true, y_pred, labels=labels).astype(float)
        cmn = self._normalize(cm, method)

        im = ax.imshow(cmn, cmap=cmap)
        ax.set_title(title, fontweight="bold")

        # --- Ajout des labels axes (PROBLÈME RÉSOLU ICI)
        ax.set_xlabel("Label prédit")
        ax.set_ylabel("Label réel")

        ax.set_xticks(range(len(labels)))
        ax.set_yticks(range(len(labels)))
        ax.set_xticklabels(class_labels)
        ax.set_yticklabels(class_labels)

        for i in range(len(labels)):
            for j in range(len(labels)):
                ax.text(j, i, f"{int(cm[i,j])}\n({cmn[i,j]:.1f}%)", ha="center")

        plt.colorbar(im, ax=ax, fraction=0.046)


    # ---------------------------------------------------------------------
    # SCÉNARIO 1 : UNE SEULE MATRICE (TEST)
    # ---------------------------------------------------------------------
    def _plot_single(self, y, y_pred, cfg):
        fig, ax = plt.subplots(figsize=cfg.single_fig_size)

        desc = self._get_normalization_description(cfg.normalization)
        self._plot_matrix(ax, y, y_pred, f"TEST — méthode={cfg.normalization}", cfg, cmap=cfg.cmap_test)

        # éviter que les labels soient coupés
        plt.tight_layout(rect=[0, 0.08, 1, 1])
        fig.subplots_adjust(bottom=0.18)

        plt.figtext(0.5, 0.02, f"Note : {desc}", ha="center", fontsize=9, color="gray")
        plt.show()
        return fig


    # ---------------------------------------------------------------------
    # SCÉNARIO 2 : VALIDATION + TEST
    # ---------------------------------------------------------------------
    def _plot_dual(self, y_test, yp_test, y_valid, yp_valid, cfg):
        fig, axes = plt.subplots(1, 2, figsize=cfg.dual_fig_size)

        desc = self._get_normalization_description(cfg.normalization)

        self._plot_matrix(
            axes[0], y_valid, yp_valid,
            title=f"VALIDATION — méthode={cfg.normalization}", config=cfg, cmap=cfg.cmap_valid
        )

        self._plot_matrix(
            axes[1], y_test, yp_test,
            title=f"TEST— méthode={cfg.normalization}", config=cfg, cmap=cfg.cmap_test
        )

        plt.tight_layout(rect=[0, 0.1, 1, 1])
        fig.subplots_adjust(bottom=0.22)

        plt.figtext(0.5, 0.03, f"Note : {desc}", ha="center", fontsize=9, color="gray")
        plt.show()
        return fig