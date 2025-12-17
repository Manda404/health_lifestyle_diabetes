import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from typing import List

from .base import BaseLearningCurvePlotter


class MatplotlibLearningCurvePlotter(BaseLearningCurvePlotter):

    def plot(
        self,
        train_scores: List[float],
        valid_scores: List[float],
        metric_name: str,
        model_name: str,
    ) -> Figure:

        epochs = range(1, len(train_scores) + 1)

        best_iteration = np.argmin(valid_scores)
        best_score = valid_scores[best_iteration]

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

        # Courbe d'apprentissage
        ax1.plot(
            epochs,
            train_scores,
            label="Train",
            linewidth=2.5,
            color="#2E86AB",
            marker="o",
            markersize=4,
            markevery=max(1, len(epochs) // 20),
            alpha=0.8,
        )

        ax1.plot(
            epochs,
            valid_scores,
            label="Validation",
            linewidth=2.5,
            color="#A23B72",
            marker="s",
            markersize=4,
            markevery=max(1, len(epochs) // 20),
            alpha=0.8,
        )

        ax1.axvline(
            x=best_iteration + 1,
            color="#06A77D",
            linestyle="--",
            linewidth=2,
            alpha=0.7,
            label=f"Meilleur modèle (iter {best_iteration+1})",
        )

        ax1.scatter(
            best_iteration + 1,
            best_score,
            color="#06A77D",
            s=200,
            zorder=5,
            edgecolors="white",
            linewidth=2,
        )

        if len(valid_scores) > best_iteration + 5:
            ax1.axvspan(
                best_iteration + 1,
                len(epochs),
                alpha=0.15,
                color="red",
                label="Zone d'overfitting potentiel",
            )

        ax1.set_xlabel("Itération (Boosting Round)", fontsize=13, fontweight="bold")
        ax1.set_ylabel(metric_name, fontsize=13, fontweight="bold")
        ax1.set_title(
            f"Courbe d'Apprentissage {model_name}",
            fontsize=15,
            fontweight="bold",
            pad=20,
        )
        ax1.legend(loc="upper right", fontsize=11)
        ax1.grid(True, alpha=0.3, linestyle="--")
        ax1.tick_params(labelsize=11)

        ax1.annotate(
            f"Meilleur: {best_score:.4f}",
            xy=(best_iteration + 1, best_score),
            xytext=(best_iteration + 1 + len(epochs) * 0.15, best_score + 0.02),
            fontsize=11,
            bbox=dict(boxstyle="round,pad=0.5", facecolor="#06A77D", alpha=0.2),
            arrowprops=dict(arrowstyle="->", color="#06A77D", lw=2),
        )

        # Gap train-validation
        gap = np.array(valid_scores) - np.array(train_scores)

        ax2.fill_between(
            epochs,
            0,
            gap,
            where=(gap >= 0),
            color="#E63946",
            alpha=0.3,
            label="Overfitting (Val > Train)",
        )

        ax2.plot(
            epochs,
            gap,
            linewidth=2.5,
            color="#E63946",
            marker="o",
            markersize=3,
            markevery=max(1, len(epochs) // 20),
        )

        ax2.axhline(y=0, color="black", linestyle="-", linewidth=1, alpha=0.3)
        ax2.axvline(
            x=best_iteration + 1,
            color="#06A77D",
            linestyle="--",
            linewidth=2,
            alpha=0.7,
        )

        ax2.set_xlabel("Itération (Boosting Round)", fontsize=13, fontweight="bold")
        ax2.set_ylabel("Écart (Validation - Train)", fontsize=13, fontweight="bold")
        ax2.set_title(
            "Gap Train-Validation (Détection Overfitting)",
            fontsize=15,
            fontweight="bold",
            pad=20,
        )
        ax2.legend(loc="upper left", fontsize=11)
        ax2.grid(True, alpha=0.3, linestyle="--")
        ax2.tick_params(labelsize=11)

        best_gap = gap[best_iteration]
        ax2.annotate(
            f"Gap optimal: {best_gap:.4f}",
            xy=(best_iteration + 1, best_gap),
            xytext=(best_iteration + 1 + len(epochs) * 0.15, best_gap + 0.005),
            fontsize=11,
            bbox=dict(boxstyle="round,pad=0.5", facecolor="yellow", alpha=0.3),
            arrowprops=dict(arrowstyle="->", color="#E63946", lw=2),
        )

        plt.tight_layout()
        plt.show()

        return fig
