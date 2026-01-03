from typing import Dict, Optional, Sequence

import matplotlib.pyplot as plt
from health_lifestyle_diabetes.domain.ports.logger_port import LoggerPort
from health_lifestyle_diabetes.domain.ports.metrics_plotter_port import (
    MetricsPlotterPort,
)


class MatplotlibMetricsPlotter(MetricsPlotterPort):
    """
    Implémentation matplotlib du MetricsPlotterPort.
    """

    DEFAULT_METRICS = ("accuracy", "precision", "recall", "f1", "auc_roc")

    def __init__(self, logger: LoggerPort):
        self.logger = logger

    def plot_metrics(
        self,
        metrics: Dict[str, float],
        *,
        title: str,
        selected_metrics: Optional[Sequence[str]] = None,
        as_percentage: bool = True,
    ) -> None:

        if selected_metrics is None:
            keys = self.DEFAULT_METRICS
        else:
            valid = [k for k in selected_metrics if k in metrics]
            invalid = [k for k in selected_metrics if k not in metrics]

            if invalid:
                self.logger.warning(
                    f"Métriques ignorées (absentes) : {invalid}"
                )

            keys = valid if valid else self.DEFAULT_METRICS

        filtered = {k: metrics[k] for k in keys if k in metrics}

        if not filtered:
            self.logger.error("Aucune métrique valide à afficher.")
            return

        values = list(filtered.values())
        labels = list(filtered.keys())
        display_values = [v * 100 if as_percentage else v for v in values]

        plt.figure(figsize=(18, 6))
        bars = plt.bar(labels, display_values, color="#007bff", alpha=0.85)

        plt.ylabel("Score (%)" if as_percentage else "Score")
        plt.title(title, fontweight="bold")

        for bar, value in zip(bars, display_values):
            plt.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height(),
                f"{value:.2f}%",
                ha="center",
                va="bottom",
                fontsize=11,
                fontweight="bold",
            )

        plt.ylim(0, max(display_values) * 1.15)
        plt.grid(axis="y", linestyle="--", alpha=0.3)
        plt.tight_layout()
        plt.show()
