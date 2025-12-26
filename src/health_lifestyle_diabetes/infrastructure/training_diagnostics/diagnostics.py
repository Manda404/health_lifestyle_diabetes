from pathlib import Path
from typing import Any, Optional

from health_lifestyle_diabetes.infrastructure.utils.config_loader import (
    YamlConfigLoader,
)
from health_lifestyle_diabetes.infrastructure.utils.paths import get_repository_root

from .metrics_extractor import BoostingMetricsExtractor
from .plotters.matplotlib import MatplotlibLearningCurvePlotter
from .plotters.plotly import PlotlyLearningCurvePlotter
from .saver import FigureSaver

# Détermine la racine du projet.
root = get_repository_root()

# Load configuration
paths = YamlConfigLoader.load_config(root / "configs/paths.yaml")
fig_path = paths["reports"]["curves_reports"]

# Extrait le chemin relatif du figure.
DEFAULT_OUTPUT_DIR = root / fig_path


class BoostingTrainingDiagnostics:
    """
    Orchestrateur des diagnostics d'entraînement boosting.
    """

    def __init__(
        self,
        model: Any,
        model_name: str, # lightgbm, xgboost, catboost
        run_name: str,   # run_catboost_001
        output_dir: Optional[str] = None,
    ):
        self.model = model
        self.model_name = model_name
        self.run_name = run_name
        self.output_dir = self.output_dir = Path(output_dir) if output_dir else Path(DEFAULT_OUTPUT_DIR)

        self.extractor = BoostingMetricsExtractor()
        self.saver = FigureSaver(output_dir=self.output_dir, run_name=self.run_name, model_name=self.model_name)
        self.plotters = {
            "matplotlib": MatplotlibLearningCurvePlotter(),
            "plotly": PlotlyLearningCurvePlotter(),
        }

    def run(self, backend: str = "matplotlib", save_figure: bool = False):

        train_scores, valid_scores, metric_name = self.extractor.extract(
            self.model, self.model_name
        )

        plotter = self.plotters.get(backend)
        if plotter is None:
            raise ValueError(f"Backend non supporté : {backend}")

        fig = plotter.plot(
            train_scores,
            valid_scores,
            metric_name,
            self.model_name
        )

        if save_figure:
            if backend == "matplotlib":
                self.saver.save_matplotlib(fig, metric_name)
            else:
                print(
                    "Plotly figure saving as image is currently not supported. "
                    "Only HTML export is available."
                )
                #self.saver.save_plotly(fig, self.model_name, metric_name)
