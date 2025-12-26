import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from .base import BaseLearningCurvePlotter


class PlotlyLearningCurvePlotter(BaseLearningCurvePlotter):

    def plot(self, train_scores, valid_scores, metric_name: str, model_name: str):

        epochs = list(range(1, len(train_scores) + 1))
        best_iteration = int(np.argmin(valid_scores))
        best_score = valid_scores[best_iteration]
        gap = np.array(valid_scores) - np.array(train_scores)

        fig = make_subplots(
            rows=1,
            cols=2,
            subplot_titles=(
                f"Courbe d'apprentissage ({metric_name})",
                "Gap Train - Validation (Overfitting)",
            ),
            column_widths=[0.6, 0.4],
            horizontal_spacing=0.12,
        )

        fig.add_trace(
            go.Scatter(
                x=epochs,
                y=train_scores,
                mode="lines+markers",
                name="Train",
                line=dict(color="#2E86AB", width=3),
                marker=dict(size=6),
            ),
            row=1,
            col=1,
        )

        fig.add_trace(
            go.Scatter(
                x=epochs,
                y=valid_scores,
                mode="lines+markers",
                name="Validation",
                line=dict(color="#A23B72", width=3),
                marker=dict(size=6),
            ),
            row=1,
            col=1,
        )

        fig.add_trace(
            go.Scatter(
                x=[best_iteration + 1],
                y=[best_score],
                mode="markers+text",
                marker=dict(
                    size=14, color="#06A77D", line=dict(color="white", width=2)
                ),
                text=[f"Best<br>{best_score:.4f}"],
                textposition="top center",
                name="Meilleur score",
            ),
            row=1,
            col=1,
        )

        fig.add_trace(
            go.Bar(
                x=epochs,
                y=gap,
                name="Gap (Val - Train)",
                marker_color="#E63946",
                opacity=0.55,
            ),
            row=1,
            col=2,
        )

        fig.add_trace(
            go.Scatter(
                x=[best_iteration + 1],
                y=[gap[best_iteration]],
                mode="markers+text",
                marker=dict(size=14, color="black", line=dict(color="white", width=2)),
                text=[f"{gap[best_iteration]:.4f}"],
                textposition="top center",
                name="Gap optimal",
            ),
            row=1,
            col=2,
        )

        fig.update_layout(
            title=dict(
                text=f"Learning Curves – {model_name}",
                x=0.5,
                font=dict(size=22, color="#333", family="Arial Black"),
            ),
            showlegend=True,
            height=600,
            template="plotly_white",
        )

        fig.update_xaxes(title_text="Itération (Boosting Round)", row=1, col=1)
        fig.update_yaxes(title_text=f"Métrique : {metric_name}", row=1, col=1)

        fig.update_xaxes(title_text="Itération (Boosting Round)", row=1, col=2)
        fig.update_yaxes(title_text="Gap (Validation - Train)", row=1, col=2)

        fig.update_traces(
            hovertemplate="<b>Itération</b>: %{x}<br><b>Valeur</b>: %{y}"
        )

        fig.show()
        return fig
