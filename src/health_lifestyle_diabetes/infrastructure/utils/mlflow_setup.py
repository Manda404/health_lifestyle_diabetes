import os
import mlflow
from mlflow.tracking import MlflowClient
from health_lifestyle_diabetes.infrastructure.utils.logger import get_logger

logger = get_logger("mlflow.setup_mlflow")
DEFAULT_EXPERIMENT = "health_lifestyle_diabetes"


def setup_mlflow(experiment_name: str | None = None, showLog: bool = False) -> str:
    """
    Configure MLflow de manière centralisée et robuste en utilisant le logger du projet.

    - Récupère l'URI de Tracking et l'emplacement des Artefacts via os.environ.
    - Crée ou active l'expérience en forçant l'emplacement des artefacts.
    - Utilise le logger interne du projet (si showLog=True).
    """

    # ============================================================
    # 1. Récupération et Vérification des Variables d'Environnement
    # ============================================================
    
    tracking_uri = os.environ.get("MLFLOW_TRACKING_URI")
    artifact_uri = os.environ.get("MLFLOW_ARTIFACT_URI")

    if not tracking_uri:
        # Sortie en cas d'erreur de configuration
        raise ValueError("MLFLOW_TRACKING_URI manquant dans l'environnement. Configuration annulée.")
        
    if not artifact_uri:
        # Sortie en cas d'erreur de configuration
        raise ValueError("MLFLOW_ARTIFACT_URI manquant dans l'environnement. Configuration annulée.")

    # ============================================================
    # 2. Configuration du Tracking et Normalisation de l'Artifact URI
    # ============================================================
    
    # 2.1. Définition de l'URI de Tracking
    mlflow.set_tracking_uri(tracking_uri)

    # 2.2. Normalisation de l'URI d'Artefact (Conversion en absolu si nécessaire)
    if not artifact_uri.startswith(('file:', 'sqlite:', 'http', 's3', 'gs')):
        absolute_path = os.path.abspath(artifact_uri)
        artifact_uri = f"file:{absolute_path}" 

    # Initialisation du client après la configuration du tracking URI
    client = MlflowClient(tracking_uri=tracking_uri)

    if showLog:
        # LOG DE VÉRIFICATION
        logger.info(f"Root system logs artefacts (URI final): {artifact_uri}") 
        logger.info(f"Tracking URI configuré: {mlflow.get_tracking_uri()}")


    # ============================================================
    # 3. Création / Récupération de l'Expérience
    # ============================================================
    
    # 3.1. Choix du nom d'expérience
    if experiment_name is None:
        experiment_name = DEFAULT_EXPERIMENT

    existing = client.get_experiment_by_name(experiment_name)

    if existing:
        exp_id = existing.experiment_id
        if showLog:
            logger.info(f"Expérience '{experiment_name}' déjà existante.")
    else:
        # Création de l'expérience en FORÇANT l'emplacement des artefacts
        exp_id = client.create_experiment(
            name=experiment_name,
            artifact_location=artifact_uri,
        )
        if showLog:
            logger.info(f"Expérience '{experiment_name}' créée avec l'ID {exp_id}.")

    # ============================================================
    # 4. Activation de l'Expérience (Méthode Anti-mlruns/)
    # ============================================================
    
    # Activation par ID d'expérience pour éviter la création de dossiers locaux.
    mlflow.set_experiment(experiment_id=exp_id)

    if showLog:
        logger.info("--- Configuration MLflow terminée avec succès ---")
        logger.info(f"Tracking URI      = {mlflow.get_tracking_uri()}")
        logger.info(f"Experiment Name   = {experiment_name}")
        logger.info(f"Experiment ID     = {exp_id}")
        logger.info(f"Artifact Location = {artifact_uri}")

    return exp_id