from typing import Dict, Optional, Sequence

import plotly.graph_objects as go
from health_lifestyle_diabetes.domain.ports.logger_port import LoggerPort
from health_lifestyle_diabetes.domain.ports.metrics_plotter_port import (
    MetricsPlotterPort,
)


class PlotlyMetricsPlotter(MetricsPlotterPort):
    """
    Implémentation Plotly du MetricsPlotterPort.

    Avantages :
    - interactive
    - compatible Streamlit / Dash
    - export HTML facile
    """

    DEFAULT_METRICS = ("accuracy", "precision", "recall", "f1", "auc_roc")

    def __init__(self, logger: LoggerPort, width: int = 1800, height: int = 600,):
        self.logger = logger
        self.width = width
        self.height = height

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

        values = [
            v * 100 if as_percentage else v for v in filtered.values()
        ]

        fig = go.Figure(
            data=[
                go.Bar(
                    x=list(filtered.keys()),
                    y=values,
                    text=[f"{v:.2f}%" for v in values],
                    textposition="auto",
                )
            ]
        )

        fig.update_layout(
            title=title,
            yaxis_title="Score (%)" if as_percentage else "Score",
            template="plotly_white",
            width=self.width,
            height=self.height,
        )

        fig.show()
