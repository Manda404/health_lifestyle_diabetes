from abc import ABC, abstractmethod
from typing import List


class BaseLearningCurvePlotter(ABC):

    @abstractmethod
    def plot(
        self,
        train_scores: List[float],
        valid_scores: List[float],
        metric_name: str,
        model_name: str,
    ):
        pass
