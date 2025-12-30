import random
import time
import uuid
from typing import Any, Dict, Iterator

import pandas as pd
from health_lifestyle_diabetes.domain.ports.dataframe_streamer_port import (
    DataFrameStreamerPort,
)
from health_lifestyle_diabetes.infrastructure.logger.loguru_logger import LoguruLogger


class PandasDataFrameStreamer(DataFrameStreamerPort):
    """
    Adapter technique pour streamer un DataFrame pandas ligne par ligne.
    """

    def __init__(self, logger=None):
        self.logger = logger or LoguruLogger()


    def stream(
        self,
        df: pd.DataFrame,
        min_delay: float,
        max_delay: float,
    ) -> Iterator[Dict[str, Any]]:

        for _, row in df.iterrows():
            # ID unique par ligne
            payload = {
                "user_id": str(uuid.uuid4()),
                **row.to_dict(),
            }
            self.logger.info(f"Envoi ligne user_id={payload['user_id']}")
            # Simule un flux temps réel
            time.sleep(random.uniform(min_delay, max_delay))

            yield payload
