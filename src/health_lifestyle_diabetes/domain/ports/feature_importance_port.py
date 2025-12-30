from typing import Protocol, Dict, Any

class FeatureImportancePort(Protocol):
    """
    Port pour l'extraction des importances de features 
    depuis n'importe quel modèle de boosting.
    """

    def get_feature_importances(self, model: Any) -> Dict[str, float]:
        """Retourne un dict {feature: importance}"""
        ...
