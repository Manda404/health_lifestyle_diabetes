from typing import Iterator, Dict, Any
import pandas as pd
from health_lifestyle_diabetes.domain.ports.dataframe_streamer_port import DataFrameStreamerPort
from health_lifestyle_diabetes.infrastructure.utils.exceptions import StreamingDataError


class DataFrameStreamerService:
    """
    Service applicatif : prépare et orchestre le streaming de DataFrame.
    """

    def __init__(self, streamer: DataFrameStreamerPort):
        self.streamer = streamer

    def run(
        self,
        df: pd.DataFrame,
        min_delay: float = 0.5,
        max_delay: float = 2.0,
    ) -> Iterator[Dict[str, Any]]:
        """
            Stream each row of a dataframe one by one with a random delay, en y ajoutant
            un identifiant utilisateur unique (UUID) placé en début de structure.

            Args:
                df (pd.DataFrame): DataFrame source.
                min_delay (float): Temps minimum entre les envois (secondes).
                max_delay (float): Temps maximum entre les envois (secondes).

            Raises:
                ValueError: Si min_delay est supérieur à max_delay.

            Yields:
                Dict[str, Any]: Un dictionnaire contenant un 'user_id' suivi 
                                des colonnes originales de la ligne.
                                Exemple :
                                {
                                    "user_id": "e2a73b0f-5768-4472-bf38-5e3b035d6c3c",
                                    "age": 45,
                                    "glucose": 132,
                                    "bmi": 29.3,
                                    ...
                                }
        """
        if min_delay > max_delay:
            raise StreamingDataError("min_delay doit être inférieur ou égal à max_delay")

        return self.streamer.stream(df, min_delay=min_delay, max_delay=max_delay)