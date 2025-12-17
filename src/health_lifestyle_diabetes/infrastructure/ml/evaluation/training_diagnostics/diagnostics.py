from pathlib import Path
from .metrics_extractor import BoostingMetricsExtractor
from .plotters.matplotlib import MatplotlibLearningCurvePlotter
from .plotters.plotly import PlotlyLearningCurvePlotter
from .saver import FigureSaver
from health_lifestyle_diabetes.infrastructure.utils.paths import get_repository_root
from health_lifestyle_diabetes.infrastructure.utils.config_loader import YamlConfigLoader

# Détermine la racine du projet.
root = get_repository_root()

# Load configuration
paths = YamlConfigLoader.load_config(root / "configs/paths.yaml")
fig_path = paths["reports"]["curves_reports"]
  
# Extrait le chemin relatif du figure.
FIGURE_PATH = root / fig_path


class BoostingTrainingDiagnostics:
    """
    Orchestrateur des diagnostics d'entraînement boosting.
    """

    def __init__(
        self,
        model,
        model_name: str,
        output_dir: Path = Path(FIGURE_PATH),
    ):
        self.model = model
        self.model_name = model_name

        self.extractor = BoostingMetricsExtractor()
        self.saver = FigureSaver(output_dir)

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
            self.model_name,
        )

        if save_figure:
            if backend == "matplotlib":
                self.saver.save_matplotlib(fig, self.model_name, metric_name)
            else:
                print(
                    "Plotly figure saving as image is currently not supported. "
                    "Only HTML export is available."
                )
                #self.saver.save_plotly(fig, self.model_name, metric_name)
