from health_lifestyle_diabetes.infrastructure.feature_engineering.pipeline_feature_engineering import (
    FeatureEngineeringPipeline,
)
from pandas import DataFrame


class BuildFeaturesUseCase:

    def __init__(self, pipeline: FeatureEngineeringPipeline):
        self.pipeline = pipeline

    def execute(
        self,
        data : DataFrame,
    ) -> DataFrame:
        return self.pipeline.transform(data)
