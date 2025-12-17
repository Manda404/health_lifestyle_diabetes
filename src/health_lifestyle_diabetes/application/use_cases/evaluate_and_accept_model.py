from dataclasses import dataclass

from health_lifestyle_diabetes.domain.services.evaluation_service import EvaluationService
from health_lifestyle_diabetes.domain.entities.evaluation_results import EvaluationResults


class ModelRejected(Exception):
    """Levée lorsque le modèle ne satisfait pas les critères métier."""


@dataclass
class EvaluateAndAcceptModelUseCase:
    """
    Use case applicatif chargé de :
    - évaluer un modèle,
    - appliquer des critères d’acceptation métier,
    - décider si le modèle est déployable ou non.
    """

    evaluation_service: EvaluationService

    # 1. POLITIQUE DE DÉCISION (application)
    max_false_negative_rate: float = 0.05
    min_recall: float = 0.90

    def execute(
        self,
        y_true,
        y_proba,
    ) -> EvaluationResults:
        """
        Évalue un modèle et décide de son acceptation.
        """

        evaluation = self.evaluation_service.evaluate(
            y_true=y_true,
            y_proba=y_proba,
        )

        # 2. Décision applicative
        if evaluation.false_negative_rate is not None:
            if evaluation.false_negative_rate > self.max_false_negative_rate:
                raise ModelRejected(
                    f"FNR trop élevé : {evaluation.false_negative_rate:.3f}"
                )

        if evaluation.recall is not None:
            if evaluation.recall < self.min_recall:
                raise ModelRejected(
                    f"Recall insuffisant : {evaluation.recall:.3f}"
                )

        return evaluation
