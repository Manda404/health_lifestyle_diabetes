from typing import Protocol, Iterator, Dict, Any
import pandas as pd


class DataFrameStreamerPort(Protocol):
    """
    Port définissant un service capable de streamer les lignes d'un DataFrame.
    """

    def stream(
        self,
        df: pd.DataFrame,
        min_delay: float,
        max_delay: float,
    ) -> Iterator[Dict[str, Any]]:
        """
        Stream les lignes d'un DataFrame avec des délais aléatoires.
        Parameters
        ----------
        df : pd.DataFrame
            DataFrame à streamer.
        min_delay : float
            Délai minimum entre deux lignes (en secondes).
        max_delay : float
            Délai maximum entre deux lignes (en secondes).
        Returns 
        -------
        Iterator[Dict[str, Any]]
            Itérateur de dictionnaires représentant les lignes du DataFrame.
        """
        ...
