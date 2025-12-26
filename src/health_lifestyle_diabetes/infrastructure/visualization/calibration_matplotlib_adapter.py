from pathlib import Path
from typing import Sequence

import matplotlib.pyplot as plt
import seaborn as sns
from health_lifestyle_diabetes.domain.ports.calibration_plot_port import (
    CalibrationPlotPort,
)
from health_lifestyle_diabetes.domain.ports.logger_port import LoggerPort
from health_lifestyle_diabetes.infrastructure.utils.config_loader import (
    YamlConfigLoader,
)
from health_lifestyle_diabetes.infrastructure.utils.paths import get_repository_root
from sklearn.calibration import calibration_curve

# === Résolution chemin sortie depuis paths.yaml ===
root = get_repository_root()
paths = YamlConfigLoader.load_config(root / "configs/paths.yaml")
OUTPUT_DIR = root / paths["reports"]["curves_reports"]
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# === Palette couleurs cohérente ===
COLOR_BEFORE = "#E74C3C"  # Rouge avant calibration
COLOR_AFTER  = "#27AE60"  # Vert après calibration
COLOR_REF    = "#34495E"  # Ligne de référence (gris bleuté)


class MatplotlibCalibrationPlotAdapter(CalibrationPlotPort):
    """
    Implémentation Matplotlib du port CalibrationPlotPort.
    Produit un plot de calibration (avant/après) pour un modèle calibré.
    """

    def __init__(self, logger: LoggerPort):
        self.logger = logger

    def plot_calibration(
        self,
        y_true: Sequence[int],
        y_proba_before: Sequence[float],
        y_proba_after: Sequence[float],
        *,
        bins: int = 10,
        model_name: str,
        save: bool = False,
    ) -> None:
        """
        Affiche une comparaison de calibration avant/après.

        Parameters
        ----------
        y_true : Sequence[int]
            Labels réels (0/1).
        y_proba_before : Sequence[float]
            Probabilités AVANT calibrage.
        y_proba_after : Sequence[float]
            Probabilités APRÈS calibrage.
        bins : int, optional
            Nombre de bins pour la courbe de calibration.
        model_name : str
            Nom du modèle (affiché dans le titre et le fichier).
        save : bool
            Si True, sauvegarde le plot dans /reports.
        """

        self.logger.info(f"Plot calibration pour le modèle '{model_name}'")

        # === Calcul des courbes ===
        fop_before, mpv_before = calibration_curve(
            y_true, y_proba_before, n_bins=bins
        )
        fop_after, mpv_after = calibration_curve(
            y_true, y_proba_after, n_bins=bins
        )

        sns.set_style("whitegrid")
        plt.figure(figsize=(16, 6))

        # ---------- Courbe de calibration ----------
        plt.subplot(1, 2, 1)
        plt.plot([0, 1], [0, 1], "--", color=COLOR_REF, label="Calibration parfaite")
        plt.plot(
            mpv_before, fop_before, "o-",
            color=COLOR_BEFORE, label="Avant calibration"
        )
        plt.plot(
            mpv_after, fop_after, "s-",
            color=COLOR_AFTER, label="Après calibration"
        )
        plt.title(f"Calibration — {model_name}")
        plt.xlabel("Probabilité prédite")
        plt.ylabel("Fraction observée de positifs")
        plt.legend()

        # ---------- Histogrammes probabilités ----------
        plt.subplot(1, 2, 2)
        sns.histplot(
            y_proba_before, bins=bins, kde=True,
            color=COLOR_BEFORE, alpha=0.5, label="Avant calibration"
        )
        sns.histplot(
            y_proba_after, bins=bins, kde=True,
            color=COLOR_AFTER, alpha=0.5, label="Après calibration"
        )
        plt.title("Distribution des probabilités")
        plt.xlabel("Probabilité prédite")
        plt.legend()

        plt.tight_layout()

        # === Sauvegarde éventuelle ===
        if save:
            outfile = OUTPUT_DIR / f"{model_name}_calibration_plot.png"
            plt.savefig(outfile, dpi=300)
            self.logger.info(f"Calibration plot sauvegardé : {outfile}")

        plt.show()
        self.logger.info("Plot de calibration terminé.")
