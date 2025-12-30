from typing import Dict, Optional
from numpy import linspace

import matplotlib.pyplot as plt
from health_lifestyle_diabetes.domain.ports.logger_port import LoggerPort
from health_lifestyle_diabetes.infrastructure.utils.config_loader import (
    YamlConfigLoader,
)
from health_lifestyle_diabetes.infrastructure.utils.paths import get_repository_root

# === Résolution chemin sortie depuis paths.yaml ===
root = get_repository_root()
paths = YamlConfigLoader.load_config(root / "configs/paths.yaml")
OUTPUT_DIR = root / paths["reports"]["curves_reports"]
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


class FeatureImportancePlotter:
    """
    Plot horizontal inversé des importances des features.
    """

    def __init__(self, logger: LoggerPort):
        self.logger = logger

    def plot(
        self,
        importances: Dict[str, float],
        top_n: Optional[int] = 20,
        model_name: Optional[str] = None,
        save_plot: bool = False,
    ):
        self.logger.info("Génération du barplot des feature importances")

        features = list(importances.keys())[:top_n]
        values = list(importances.values())[:top_n]

        # Couleurs progressives (du rouge vers le bleu)
        #colors = plt.cm.viridis(linspace(0, 1, len(features)))

        plt.figure(figsize=(18, max(6, len(features) * 0.4)))
        plt.barh(features[::-1], values[::-1], color="#1f77b4")
        plt.xlabel("Importance")
        plt.ylabel("Features")
        plt.title(f"Top {top_n} Features — {model_name or ''}".strip())
        plt.tight_layout()

        if save_plot:
            if model_name:
                filename = f"feature_importances_{model_name.lower().replace(' ', '_')}.png"
            else:
                filename = "feature_importances.png"
            plt.savefig(OUTPUT_DIR / filename, dpi=300)
            self.logger.info(f"Figure sauvegardée ➜ {OUTPUT_DIR / filename}")

        plt.show()
        self.logger.info("Affichage du barplot des feature importances terminé")
        plt.close()
