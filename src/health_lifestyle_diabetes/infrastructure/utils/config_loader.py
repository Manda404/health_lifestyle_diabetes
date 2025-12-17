"""
config_loader.py
-----------------

Utilitaire pour charger des fichiers de configuration YAML.

Objectifs :
- Centraliser la logique de lecture/validation des fichiers YAML.
- Fournir une méthode simple : load_config("training.yaml")
- Gérer les erreurs proprement via ConfigLoadingError.
"""

from pathlib import Path
from typing import Any, Dict

import yaml

from .exceptions import ConfigLoadingError


class YamlConfigLoader:
    """
    Classe statique responsable du chargement et de la validation des fichiers YAML.
    """

    @staticmethod
    def load_config(config_path: str | Path) -> Dict[str, Any]:
        """
        Charge un fichier YAML et retourne un dictionnaire.

        Parameters
        ----------
        config_path : str | Path
            Chemin vers le fichier de configuration.

        Returns
        -------
        Dict[str, Any]
            Configuration sous forme de dictionnaire Python.

        Raises
        ------
        ConfigLoadingError
            Si le fichier n'existe pas, est mal formé ou inaccessible.
        """
        path = Path(config_path)

        if not path.exists():
            raise ConfigLoadingError(
                f"Le fichier de configuration '{path}' est introuvable."
            )

        try:
            with open(path, "r", encoding="utf-8") as file:
                config = yaml.safe_load(file)

            if config is None:
                raise ConfigLoadingError(
                    f"Le fichier '{path}' est vide ou mal structuré."
                )

            return config

        except yaml.YAMLError as exc:
            raise ConfigLoadingError(
                f"Erreur YAML lors du chargement du fichier '{path}': {exc}"
            )

        except Exception as exc:
            raise ConfigLoadingError(
                f"Une erreur est survenue lors du chargement du fichier '{path}': {exc}"
            )
