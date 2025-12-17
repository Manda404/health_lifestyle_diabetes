from domain.services.evaluation_service import EvaluationService
from infrastructure.ml.metrics.sklearn_metrics_adapter import SklearnMetricsAdapter

def evaluate_model(y_true, y_proba, threshold=0.5):
    """
    Use case applicatif d'évaluation de modèle.
    """

    # 1️⃣ Infrastructure branchée
    metrics_adapter = SklearnMetricsAdapter()

    # 2️⃣ Domaine instancié
    evaluation_service = EvaluationService(
        metrics_port=metrics_adapter,
        threshold=threshold,
    )

    # 3️⃣ Exécution du métier
    return evaluation_service.evaluate(
        y_true=y_true,
        y_proba=y_proba,
    )
