from typing import Any, Dict
from health_lifestyle_diabetes.domain.ports.feature_importance_port import (
    FeatureImportancePort,
)


class BoostingFeatureImportanceAdapter(FeatureImportancePort):
    """
    Extraction des importances pour modèles XGBoost, LightGBM, CatBoost.
    """

    def get_feature_importances(self, model: Any) -> Dict[str, float]:
        module_name = type(model).__module__

        # ======================
        # XGBoost
        # ======================
        if hasattr(model, "get_booster") and "xgboost" in module_name:
            booster = model.get_booster()
            scores = booster.get_score(importance_type="gain")  # {fN: importance}
            return dict(sorted(scores.items(), key=lambda x: x[1], reverse=True))

        # ======================
        # CatBoost
        # ======================
        if hasattr(model, "get_feature_importance") and "catboost" in module_name:
            importances = model.get_feature_importance()  # type: ignore

            try:
                feature_names = list(model.feature_names_)
            except AttributeError:
                # fallback si pas de noms récupérables
                feature_names = [f"feature_{i}" for i in range(len(importances))]

            return {
                name: score
                for name, score in sorted(
                    zip(feature_names, importances),
                    key=lambda x: x[1],
                    reverse=True
                )
            }

        # ======================
        # LightGBM
        # ======================
        if hasattr(model, "feature_importances_") and "lightgbm" in module_name:
            feature_names = list(model.feature_name_)
            importances = list(model.feature_importances_)
            return {
                name: score
                for name, score in sorted(
                    zip(feature_names, importances),
                    key=lambda x: x[1],
                    reverse=True
                )
            }

        # ======================
        # Non supporté
        # ======================
        raise ValueError(
            f"Modèle non supporté pour l'extraction des importances : {type(model)}"
        )
