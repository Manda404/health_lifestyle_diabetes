from pathlib import Path


class FigureSaver:

    def __init__(self, output_dir: Path, run_name: str, model_name: str):
        self.output_dir = output_dir
        self.run_name = run_name
        self.model_name = model_name
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def save_matplotlib(self, fig, metric_name: str):
        path = self.output_dir / f"{self.run_name}_{self.model_name}_{metric_name}_learning_curve.png"
        fig.savefig(path, dpi=300)

    def save_plotly(self, fig, metric_name: str):
        png = self.output_dir / f"{self.run_name}_{self.model_name}_{metric_name}_learning_curve.png"
        html = self.output_dir / f"{self.run_name}_{self.model_name}_{metric_name}.html"

        fig.write_image(str(png), scale=2)
        fig.write_html(str(html))
