from typing import Any, Dict, List, Optional, Tuple


class BoostingMetricsExtractor:
    """
    Extraction des métriques d'entraînement / validation
    pour modèles de boosting.
    """

    def extract(
        self, model: Any, model_name: str
    ) -> Tuple[List[float], List[float], str]:

        evals_result: Optional[Dict] = None
        model_type = model_name.lower()

        if model_type == "lightgbm":
            evals_result = model.evals_result_
            train_key, valid_key = "train", "valid"

        elif model_type == "xgboost":
            evals_result = model.evals_result()
            train_key, valid_key = "validation_0", "validation_1"

        elif model_type == "catboost":
            evals_result = model.get_evals_result()
            train_key, valid_key = "learn", "validation" #'learn', 'validation'

        else:
            raise ValueError(f"Modèle non supporté : {model_name}")

        if evals_result is None:
            raise ValueError("Aucune métrique d'évaluation disponible.")

        metric_name = list(evals_result[train_key].keys())[0]

        return (
            evals_result[train_key][metric_name],
            evals_result[valid_key][metric_name],
            metric_name,
        )
