# ⚕️ Health & Lifestyle Diabetes Prediction

**Un projet Machine Learning pédagogique basé sur la Clean Architecture et les bonnes pratiques MLOps**

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Poetry](https://img.shields.io/badge/Poetry-Dependency%20Management-blue)](https://python-poetry.org/)
[![MLflow](https://img.shields.io/badge/MLflow-Experiment%20Tracking-blue)](https://mlflow.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-API%20Framework-green)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📋 Présentation

Ce projet démontre **comment structurer un système de Machine Learning de manière professionnelle** en appliquant les principes de la Clean Architecture aux projets de Data Science.

**Dataset** : [Health & Lifestyle Data for Diabetes Prediction](https://www.kaggle.com/datasets/alamshihab075/health-and-lifestyle-data-for-diabetes-prediction)

**Objectif** : Prédiction du diabète (classification binaire, multi-classes, estimation de risque) à partir de données de santé et de mode de vie.

**Valeur ajoutée** : Architecture logicielle robuste, séparation claire des responsabilités, workflow MLOps complet, code maintenable et testable.

---

## 🎯 Ce que j'ai réalisé

### Architecture & Design
- Application de la **Clean Architecture** à un projet de Data Science complet
- Séparation stricte en 4 couches : Domain, Application, Infrastructure, Presentation
- Inversion des dépendances pour un code découplé et évolutif
- Structure modulaire permettant de changer facilement de modèle ou de source de données

### Pipeline Machine Learning
- Implémentation de modèles de boosting (Gradient Boosting, XGBoost, CatBoost)
- Feature engineering avec pipeline de preprocessing modulaire
- Training pipeline avec validation croisée et early stopping
- Évaluation multi-métriques (accuracy, precision, recall, F1-score, ROC-AUC)

### Pratiques MLOps

**Tracking & Reproductibilité**
- Tracking complet des expériences avec MLflow
- Versioning automatique des modèles et artifacts
- Configuration externalisée en YAML (aucun paramètre codé en dur)
- Gestion des random seeds pour garantir la reproductibilité

**Infrastructure & Production**
- API REST avec FastAPI (documentation OpenAPI automatique)
- Validation des données d'entrée avec Pydantic
- Gestion robuste des erreurs et logging structuré
- Interface CLI pour l'entraînement et l'évaluation

**Qualité & Tests**
- Suite de tests complète (unit, integration, e2e)
- CI/CD avec GitHub Actions (tests automatisés, linting, formatting)
- Code coverage et analyse statique
- Type hints et validation mypy

---

## 🏗️ Architecture du projet

```
presentation  →  application  →  domain
        ↑                ↑
        └──── infrastructure ─┘
```

**Domain** : Entités métier, interfaces, règles business (indépendant de toute technologie)

**Application** : Cas d'usage (TrainingUseCase, PredictionUseCase, EvaluationUseCase)

**Infrastructure** : Implémentations concrètes (data loaders, modèles ML, preprocessing, tracking MLflow)

**Presentation** : Interfaces d'exposition (API REST, CLI, dashboard)

Cette architecture garantit que le cœur métier reste stable même si l'infrastructure technique change.

---

## 📁 Structure du code

```
health_lifestyle_diabetes/
├── configs/
│   ├── training.yaml          # Hyperparamètres et configuration d'entraînement
│   ├── inference.yaml         # Configuration pour l'inférence
│   ├── preprocessing.yaml     # Pipeline de feature engineering
│   └── paths.yaml             # Chemins des données et modèles
├── tests/
│   ├── domain/                # Tests de la logique métier
│   ├── application/           # Tests des cas d'usage
│   ├── infrastructure/        # Tests des implémentations
│   └── e2e/                   # Tests end-to-end
└── src/health_lifestyle_diabetes/
    ├── domain/
    │   ├── entities/          # Modèles de données métier
    │   ├── repositories/      # Interfaces abstraites
    │   └── services/          # Services métier
    ├── application/
    │   └── use_cases/         # Training, Prediction, Evaluation
    ├── infrastructure/
    │   ├── data/              # Data loaders et persistance
    │   ├── models/            # Wrappers des modèles ML
    │   ├── preprocessing/     # Feature engineering
    │   └── tracking/          # MLflow integration
    └── presentation/
        ├── api/               # FastAPI endpoints
        └── cli/               # Command Line Interface
```

---

## 🛠️ Stack technique

### Core ML
- **Pandas, NumPy** : Manipulation et calcul sur données tabulaires
- **Scikit-learn** : Preprocessing, pipelines, métriques
- **XGBoost, CatBoost** : Modèles de boosting optimisés

### MLOps & Engineering
- **MLflow** : Tracking d'expériences, versioning de modèles, registry
- **FastAPI** : API REST moderne et performante
- **Pydantic** : Validation de données et serialization
- **Poetry** : Gestion des dépendances et packaging

### DevOps & Qualité
- **GitHub Actions** : CI/CD automatisé
- **pytest** : Framework de tests complet
- **ruff** : Linting rapide et moderne
- **black** : Formatage automatique du code
- **mypy** : Vérification statique des types

### Configuration & Logging
- **YAML** : Configuration déclarative externalisée
- **Python logging** : Logging structuré avec rotation

---

## 🚀 Utilisation

### Installation

```bash
# Cloner le repository
git clone https://github.com/votre-username/health-lifestyle-diabetes.git
cd health-lifestyle-diabetes

# Installer les dépendances avec Poetry
poetry install
poetry shell
```

### Entraînement

```bash
# Entraîner un modèle avec tracking MLflow
poetry run python -m health_lifestyle_diabetes.presentation.cli train --config configs/training.yaml

# Voir les résultats dans MLflow UI
mlflow ui
```

### Inférence via API

```bash
# Lancer l'API FastAPI
poetry run uvicorn health_lifestyle_diabetes.presentation.api.main:app --reload

# Documentation interactive disponible sur http://localhost:8000/docs
```

### Tests et qualité

```bash
# Exécuter la suite de tests
poetry run pytest

# Vérifier le code
poetry run ruff check .
poetry run black --check .
poetry run mypy src/
```

---

## 💡 Pourquoi ce projet est différent

**Pas un simple notebook Jupyter**
Ce projet montre comment structurer du code ML pour la production, avec une architecture qui facilite la maintenance, les tests et l'évolution.

**Séparation claire des responsabilités**
Chaque composant a un rôle précis. Changer de modèle, de source de données ou d'API n'impacte qu'une seule couche.

**MLOps par défaut**
Le tracking, le versioning, la reproductibilité et la qualité du code ne sont pas des ajouts après coup, mais intégrés dès la conception.

**Testable et évolutif**
L'architecture permet d'écrire des tests à tous les niveaux et de faire évoluer le système sans tout casser.

---

## 🎓 Compétences démontrées

- Application de principes d'architecture logicielle à la Data Science
- Mise en place d'un workflow MLOps complet (tracking, versioning, CI/CD)
- Design de code découplé, testable et maintenable
- Exposition de modèles ML via API REST professionnelle
- Configuration externalisée et gestion de la reproductibilité
- Pratiques DevOps appliquées au Machine Learning

---

## 👤 Auteur

**Rostand Surel**  
📧 [rostandsurel@yahoo.com](mailto:rostandsurel@yahoo.com)

---

## 📄 Licence

Ce projet est sous licence MIT.