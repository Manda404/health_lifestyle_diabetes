from datetime import datetime
from pathlib import Path


class FigureSaver:

    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def save_matplotlib(self, fig, model_name: str, metric_name: str):
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = self.output_dir / f"{ts}_{model_name}_{metric_name}_learning_curve.png"
        fig.savefig(path, dpi=300)

    def save_plotly(self, fig, model_name: str, metric_name: str):
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        png = self.output_dir / f"{ts}_{model_name}_{metric_name}_learning_curve.png"
        html = self.output_dir / f"{ts}_{model_name}_{metric_name}.html"

        fig.write_image(str(png), scale=2)
        fig.write_html(str(html))
