"""
poetry run mlflow ui \
  --backend-store-uri $MLFLOW_TRACKING_URI \
  --default-artifact-root $MLFLOW_ARTIFACT_URI


poetry run mlflow ui \
  --backend-store-uri $MLFLOW_TRACKING_URI \
  --default-artifact-root $MLFLOW_ARTIFACT_URI \
  --port 5002

  
poetry run mlflow ui \
  --backend-store-uri $MLFLOW_TRACKING_URI \
  --default-artifact-root $MLFLOW_ARTIFACT_URI \
  --host 0.0.0.0 \
  --port 5002

"""