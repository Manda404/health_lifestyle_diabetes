import numpy as np
from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from matplotlib.figure import Figure
from plotly.subplots import make_subplots
from typing import Any, Tuple, List, Optional, Dict
from health_lifestyle_diabetes.infrastructure.utils.config_loader import ConfigLoader
from health_lifestyle_diabetes.infrastructure.utils.paths import get_repository_root

root = get_repository_root()
paths = ConfigLoader.load_config(root / "configs/paths.yaml")


class LearningCurvePlotter:

    def __get_training_metrics(self, model: Any, model_name:str ) -> Tuple[List[float], List[float], str]:
        """
        Récupère les métriques d’entraînement et de validation pour chaque itération,
        en fonction du type de modèle utilisé (LightGBM, XGBoost ou CatBoost).

        Retourne
        --------
        train_scores : list[float]
            Valeurs de la métrique à chaque itération sur l’ensemble d’entraînement.
        valid_scores : list[float]
            Valeurs de la métrique à chaque itération sur l’ensemble de validation.
        metric_name : str
            Nom de la métrique surveillée (ex. : "logloss").

        Soulève
        -------
        ValueError
            Si le type de modèle n’est pas supporté ou si aucune métrique n’est disponible.
        """

        evals_result: Optional[Dict[str, Dict[str, list[Any]]]] = None

        # Extraction selon le modèle
        model_type = model_name.lower()

        if model_type == "lightgbm":
            evals_result = model.evals_result_
            train_key, valid_key = "train", "valid"

        elif model_type == "xgboost":
            evals_result = model.evals_result()
            train_key, valid_key = "validation_0", "validation_1"

        elif model_type == "catboost":
            evals_result = model.get_evals_result()
            train_key, valid_key = "learn", "validation"

        else:
            raise ValueError("Modèle non supporté : doit être LightGBM, XGBoost ou CatBoost.")

        # Vérification des résultats d’évaluation
        if evals_result is None:
            raise ValueError("Aucune métrique d'évaluation disponible pour ce modèle.")

        # Première métrique disponible (logloss, accuracy...)
        metric_name = list(evals_result[train_key].keys())[0]

        # Retour des valeurs itération par itération
        return (
            evals_result[train_key][metric_name],   # scores entraînement
            evals_result[valid_key][metric_name],   # scores validation
            metric_name,                            # nom de la métrique
        )

    def __plot_learning_curves_interactive(
        self,
        train_scores,
        valid_scores,
        metric_name: str,
        model_name: str,
    ):
        """
        Courbes d'apprentissage interactives Plotly + visualisation du gap Train/Validation.
        """

        epochs = list(range(1, len(train_scores) + 1))
        best_iteration = int(np.argmin(valid_scores))
        best_score = valid_scores[best_iteration]
        gap = np.array(valid_scores) - np.array(train_scores)

        # --- Layout global
        fig = make_subplots(
            rows=1,
            cols=2,
            subplot_titles=(
                f"Courbe d'apprentissage ({metric_name})",
                "Gap Train - Validation (Overfitting)",
            ),
            column_widths=[0.6, 0.4],
            horizontal_spacing=0.12
        )

        # --------------------------------------------------------
        # 📈 1) Courbe d'apprentissage
        # --------------------------------------------------------
        fig.add_trace(
            go.Scatter(
                x=epochs,
                y=train_scores,
                mode="lines+markers",
                name="Train",
                line=dict(color="#2E86AB", width=3),
                marker=dict(size=6),
            ),
            row=1, col=1
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
            row=1, col=1
        )

        # Meilleure itération
        fig.add_trace(
            go.Scatter(
                x=[best_iteration + 1],
                y=[best_score],
                mode="markers+text",
                marker=dict(size=14, color="#06A77D", line=dict(color="white", width=2)),
                text=[f"Best<br>{best_score:.4f}"],
                textposition="top center",
                name="Meilleur score",
            ),
            row=1, col=1
        )

        # --------------------------------------------------------
        # 🔥 2) Gap Train - Validation (overfitting)
        # --------------------------------------------------------
        fig.add_trace(
            go.Bar(
                x=epochs,
                y=gap,
                name="Gap (Val - Train)",
                marker_color="#E63946",
                opacity=0.55,
            ),
            row=1, col=2
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
            row=1, col=2
        )

        # --------------------------------------------------------
        # 🎨 Mise en forme
        # --------------------------------------------------------
        fig.update_layout(
            title=dict(
                text=f"Learning Curves – {model_name}",
                x=0.5,
                font=dict(size=22, color="#333", family="Arial Black")
            ),
            showlegend=True,
            height=600,
            template="plotly_white",
        )

        fig.update_xaxes(title_text="Itération (Boosting Round)", row=1, col=1)
        fig.update_yaxes(title_text=f"Métrique : {metric_name}", row=1, col=1)

        fig.update_xaxes(title_text="Itération (Boosting Round)", row=1, col=2)
        fig.update_yaxes(title_text="Gap (Validation - Train)", row=1, col=2)

        fig.update_traces(hovertemplate="<b>Itération</b>: %{x}<br><b>Valeur</b>: %{y}")

        fig.show()

        return fig

    def __plot_learning_curves(self, train_scores: List[float], valid_scores: List[float], metric_name:str, model_name:str) -> Figure:
        """
        Visualise les courbes d'apprentissage et le gap train-validation.
        
        Parameters:
        -----------
        train_scores : list or array
            Scores sur l'ensemble d'entraînement pour chaque itération
        valid_scores : list or array
            Scores sur l'ensemble de validation pour chaque itération
        metric_name : str
            Nom de la métrique (ex: 'Log Loss', 'RMSE', 'Accuracy')
        model_name : str, optional
            Nom du modèle pour le titre (default: 'Model')
        
        Returns:
        --------
        Figure
            La figure matplotlib générée
        """
        epochs = range(1, len(train_scores) + 1)

        best_iteration = np.argmin(valid_scores)
        best_score = valid_scores[best_iteration]

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

        # Courbe d'apprentissage
        ax1.plot(epochs, train_scores, label='Train', linewidth=2.5,
                color='#2E86AB', marker='o', markersize=4,
                markevery=max(1, len(epochs)//20), alpha=0.8)

        ax1.plot(epochs, valid_scores, label='Validation', linewidth=2.5,
                color='#A23B72', marker='s', markersize=4,
                markevery=max(1, len(epochs)//20), alpha=0.8)

        ax1.axvline(x=best_iteration + 1, color='#06A77D', linestyle='--',
                    linewidth=2, alpha=0.7, label=f'Meilleur modèle (iter {best_iteration+1})')

        ax1.scatter(best_iteration + 1, best_score, color='#06A77D',
                    s=200, zorder=5, edgecolors='white', linewidth=2)

        if len(valid_scores) > best_iteration + 5:
            ax1.axvspan(best_iteration + 1, len(epochs),
                        alpha=0.15, color='red', label='Zone d\'overfitting potentiel')

        ax1.set_xlabel('Itération (Boosting Round)', fontsize=13, fontweight='bold')
        #ax1.set_ylabel('Log Loss', fontsize=13, fontweight='bold')
        ax1.set_ylabel(f'{metric_name}', fontsize=13, fontweight='bold')
        ax1.set_title(f'Courbe d\'Apprentissage {model_name}', fontsize=15, fontweight='bold', pad=20)
        ax1.legend(loc='upper right', fontsize=11)
        ax1.grid(True, alpha=0.3, linestyle='--')
        ax1.tick_params(labelsize=11)

        ax1.annotate(f'Meilleur: {best_score:.4f}',
                    xy=(best_iteration+1, best_score),
                    xytext=(best_iteration+1 + len(epochs)*0.15, best_score + 0.02),
                    fontsize=11,
                    bbox=dict(boxstyle='round,pad=0.5', facecolor='#06A77D', alpha=0.2),
                    arrowprops=dict(arrowstyle='->', color='#06A77D', lw=2))

        # Gap train-val
        gap = np.array(valid_scores) - np.array(train_scores)

        ax2.fill_between(epochs, 0, gap, where=(gap >= 0),
                        color='#E63946', alpha=0.3, label='Overfitting (Val > Train)')

        ax2.plot(epochs, gap, linewidth=2.5, color='#E63946',
                marker='o', markersize=3,
                markevery=max(1, len(epochs)//20))

        ax2.axhline(y=0, color='black', linestyle='-', linewidth=1, alpha=0.3)
        ax2.axvline(x=best_iteration + 1, color='#06A77D',
                    linestyle='--', linewidth=2, alpha=0.7)

        ax2.set_xlabel('Itération (Boosting Round)', fontsize=13, fontweight='bold')
        ax2.set_ylabel('Écart (Validation - Train)', fontsize=13, fontweight='bold')
        ax2.set_title('Gap Train-Validation (Détection Overfitting)', fontsize=15, fontweight='bold', pad=20)
        ax2.legend(loc='upper left', fontsize=11)
        ax2.grid(True, alpha=0.3, linestyle='--')
        ax2.tick_params(labelsize=11)

        best_gap = gap[best_iteration]
        ax2.annotate(f'Gap optimal: {best_gap:.4f}',
                    xy=(best_iteration + 1, best_gap),
                    xytext=(best_iteration + 1 + len(epochs)*0.15, best_gap + 0.005),
                    fontsize=11,
                    bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.3),
                    arrowprops=dict(arrowstyle='->', color='#E63946', lw=2))

        plt.tight_layout()
        plt.show()
        
        return fig

    def __save_plotly_figure(self, fig, model_name: str, metric_name: str) -> None:
        """
        Sauvegarde une figure Plotly au format PNG et HTML.
        """
        save_dir = Path(Path(root / paths["reports"]["curves_reports"]))
        save_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        png_path = save_dir / f"{timestamp}_{model_name.lower()}_{metric_name}_learning_curve.png"
        html_path = save_dir / f"{timestamp}_{model_name.lower()}_{metric_name}_learning_curve.html"

        # --- Sauvegarde image PNG ---
        fig.write_image(str(png_path), format="png", scale=2)

        # --- Sauvegarde interactive HTML ---
        fig.write_html(str(html_path))

    def __save_plotlib_figure(self, fig, model_name: str, metric_name: str) -> None:
        """
        Sauvegarde une figure Plotly au format PNG et HTML.
        """
        save_dir = Path(Path(root / paths["reports"]["curves_reports"]))
        save_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        png_path = save_dir / f"{timestamp}_{model_name.lower()}_{metric_name}_learning_curve.png"

        # --- Sauvegarde image PNG ---
        fig.savefig(png_path, format='png', dpi=300)


    def plot_training_diagnostics(self, model, model_name: str, save_figure: bool = True):
        """
        Trace les courbes d'apprentissage provenant du modèle boosting.
        Compatible XGBoost, CatBoost, LightGBM.
        """
        # Extraire les informations de d'entrainement pour la visualisation
        train_scores, valid_scores, metric_name = self.__get_training_metrics(model, model_name)

        # Visualise les courbes d'apprentissage et le gap train-validation.
        fig = self.__plot_learning_curves(train_scores, valid_scores, metric_name, model_name)

        # ---------------------------------------------------
        # Sauvegarde locale
        # ---------------------------------------------------
        if save_figure:
            self.__save_plotlib_figure(fig, model_name, metric_name)
        
        plt.close(fig)


