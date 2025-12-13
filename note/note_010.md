```text
health_lifestyle_diabetes/
│
├── domain/
│   ├── entities/
│   │   ├── patient_profile.py
│   │   ├── prediction_output.py
│   │   ├── feature_schema.py
│   │   └── evaluation_results.py
│   │
│   ├── ports/
│   │   ├── dataset_repository_port.py
│   │   ├── model_repository_port.py
│   │   ├── model_trainer_port.py
│   │   ├── feature_engineering_port.py
│   │   └── evaluation_metric_port.py   ← NOUVEAU
│   │
│   └── services/
│       ├── feature_validation_service.py
│       ├── prediction_service.py
│       ├── evaluation_service.py        ← LOGIQUE METIER
│       ├── threshold_service.py         ← seuil & FP/FN
│       └── calibration_service.py       ← Binning métier
│
│
├── application/
│   ├── dto/
│   │   ├── training_config.py
│   │   ├── evaluation_request.py
│   │   ├── evaluation_response.py
│   │   ├── prediction_request.py
│   │   └── prediction_response.py
│   │
│   └── use_cases/
│       ├── train_model.py
│       ├── evaluate_model.py        ← ORCHESTRATION CENTRALE
│       ├── preprocess_dataset.py
│       ├── perform_eda.py
│       └── predict_patient.py
│
│
├── infrastructure/
│   ├── data_sources/
│   │   ├── csv_dataset_repository.py
│   │   └── local_storage.py
│   │
│   ├── repositories/
│   │   ├── dataset_repository_impl.py
│   │   └── model_repository_impl.py
│   │
│   ├── ml/
│   │   ├── trainers/
│   │   │   ├── catboost_trainer.py
│   │   │   ├── xgboost_trainer.py
│   │   │   └── lightgbm_trainer.py
│   │   │
│   │   ├── feature_engineering/
│   │   │   ├── base_preprocessing.py
│   │   │   ├── clinical_features.py
│   │   │   ├── lifestyle_features.py
│   │   │   ├── medical_features.py
│   │   │   └── pipeline_feature_engineering.py
│   │   │
│   │   ├── evaluation/
│   │   │   ├── confusion_matrix_plotter.py
│   │   │   ├── roc_plotter.py
│   │   │   ├── pr_plotter.py
│   │   │   ├── probability_plotter.py
│   │   │   └── calibration_curve_plotter.py
│   │   │
│   │   ├── metrics/
│   │   │   ├── sklearn_metrics_adapter.py
│   │   │   └── calibration_adapter.py
│   │   │
│   │   └── pipelines/
│   │       └── diabetes_pipeline.py
│   │
│   └── utils/
│       ├── logger.py
│       ├── config_loader.py
│       └── paths.py
│
│
└── presentation/
    ├── cli/
    │   ├── train.py
    │   ├── evaluate.py
    │   └── predict.py
    │
    ├── api/
    │   └── fastapi_app.py
    │
    └── streamlit/
        └── dashboard.py
```