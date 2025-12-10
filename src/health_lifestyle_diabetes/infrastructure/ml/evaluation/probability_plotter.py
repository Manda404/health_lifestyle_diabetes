# src/health_lifestyle_diabetes/infrastructure/ml/evaluation/probability_plotter.py

import matplotlib.pyplot as plt
import seaborn as sns
from health_lifestyle_diabetes.infrastructure.utils.logger import get_logger
from sklearn.calibration import calibration_curve

logger = get_logger("evaluation.probability_plotter")


class ProbabilityPlotter:
    """
    Plots indispensables pour analyser la distribution des probabilités prédites.
    Chaque plot est loggé pour tracer l'exécution.
    """

    # =====================================================================
    @staticmethod
    def plot_global_probability_distribution(model, X):
        logger.info("Plot: Distribution globale des probabilités — démarrage.")
        probas = model.predict_proba(X)[:, 1]

        logger.debug(
            f"Probabilités min={probas.min():.4f}, max={probas.max():.4f}, mean={probas.mean():.4f}"
        )

        plt.figure(figsize=(8, 5))
        sns.histplot(probas, kde=True, bins=30)

        plt.title("Distribution globale des probabilités prédites")
        plt.xlabel("Probabilité prédite (classe positive)")
        plt.ylabel("Fréquence")
        plt.grid(True, linestyle="--", alpha=0.3)
        plt.show()

        logger.info("Plot: Distribution globale des probabilités — terminé.")

    # =====================================================================
    @staticmethod
    def plot_probability_by_true_class(model, X, y):
        logger.info("Plot: Distribution par classe réelle — démarrage.")
        probas = model.predict_proba(X)[:, 1]

        logger.debug(
            f"Stats classe 0 — mean={probas[y==0].mean():.4f}, std={probas[y==0].std():.4f}, n={len(probas[y==0])}"
        )
        logger.debug(
            f"Stats classe 1 — mean={probas[y==1].mean():.4f}, std={probas[y==1].std():.4f}, n={len(probas[y==1])}"
        )

        plt.figure(figsize=(9, 5))
        sns.kdeplot(probas[y == 0], fill=True, alpha=0.5, label="Classe réelle : 0")
        sns.kdeplot(probas[y == 1], fill=True, alpha=0.5, label="Classe réelle : 1")

        plt.title("Distribution des probabilités selon la classe réelle")
        plt.xlabel("Probabilité prédite (classe positive)")
        plt.ylabel("Densité")
        plt.legend()
        plt.grid(True, linestyle="--", alpha=0.3)
        plt.show()

        logger.info("Plot: Distribution par classe réelle — terminé.")

    # =====================================================================
    @staticmethod
    def plot_fp_fn_distribution(model, X, y, threshold: float = 0.5):
        logger.info("Plot: Distribution FP/FN — démarrage.")
        probas = model.predict_proba(X)[:, 1]
        preds = (probas >= threshold).astype(int)

        fp = probas[(preds == 1) & (y == 0)]
        fn = probas[(preds == 0) & (y == 1)]

        logger.debug(f"Nombre de FP = {len(fp)}, Nombre de FN = {len(fn)}")

        plt.figure(figsize=(9, 5))
        if len(fp) > 0:
            sns.kdeplot(fp, fill=True, label="Faux positifs (FP)", alpha=0.6)
        if len(fn) > 0:
            sns.kdeplot(fn, fill=True, label="Faux négatifs (FN)", alpha=0.6)

        plt.title("Distribution des probabilités des FP et FN")
        plt.xlabel("Probabilité prédite")
        plt.ylabel("Densité")
        plt.legend()
        plt.grid(True, linestyle="--", alpha=0.3)
        plt.show()

        logger.info("Plot: Distribution FP/FN — terminé.")

    # =====================================================================
    @staticmethod
    def plot_calibration_curve(model, X, y, n_bins: int = 10):
        logger.info("Plot: Calibration curve — démarrage.")
        probas = model.predict_proba(X)[:, 1]
        frac_pos, mean_pred = calibration_curve(y, probas, n_bins=n_bins)

        logger.debug("Calibration — points calculés")
        logger.debug(f"mean_pred: {mean_pred}")
        logger.debug(f"frac_pos: {frac_pos}")

        plt.figure(figsize=(7, 6))
        plt.plot(mean_pred, frac_pos, marker="o", label="Calibration du modèle")
        plt.plot([0, 1], [0, 1], linestyle="--", color="gray", label="Idéal")

        plt.title("Calibration Curve")
        plt.xlabel("Probabilité prédite")
        plt.ylabel("Fréquence réelle observée")
        plt.legend()
        plt.grid(True, linestyle="--", alpha=0.3)
        plt.show()

        logger.info("Plot: Calibration curve — terminé.")

    # =====================================================================
    @staticmethod
    def plot_threshold_view(model, X, threshold: float = 0.5):
        logger.info("Plot: Vue du seuil — démarrage.")
        probas = model.predict_proba(X)[:, 1]

        logger.debug(f"Seuil actuel = {threshold}, mean proba = {probas.mean():.4f}")

        plt.figure(figsize=(8, 5))
        sns.histplot(probas, kde=True, bins=40, alpha=0.6)
        plt.axvline(
            threshold, color="red", linestyle="--", label=f"Seuil = {threshold:.2f}"
        )

        plt.title("Distribution des probabilités et seuil de décision")
        plt.xlabel("Probabilité prédite")
        plt.ylabel("Fréquence")
        plt.legend()
        plt.grid(True, linestyle="--", alpha=0.3)
        plt.show()

        logger.info("Plot: Vue du seuil — terminé.")
