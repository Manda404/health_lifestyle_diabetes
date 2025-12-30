from health_lifestyle_diabetes.domain.ports.dataset_repository_port import (
    DatasetRepositoryPort,
)
from health_lifestyle_diabetes.domain.ports.logger_port import LoggerPort
from pandas import DataFrame


class LoadDatasetUseCase:
    """
    Use Case : Charger un dataset depuis la source configurée.
    """

    def __init__(self, repository: DatasetRepositoryPort, logger: LoggerPort):
        self.repository = repository
        self.logger = logger

    def execute(self) -> DataFrame:
        self.logger.info("Démarrage du chargement du dataset...")
        data = self.repository.load_dataset()
        self.logger.info(f"Dataset chargé : {data.shape[0]} lignes, {data.shape[1]} colonnes.")
        return data
