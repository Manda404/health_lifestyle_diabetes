# 🎓 OBJECTIF PÉDAGOGIQUE

À la fin de cette explication, tu dois être capable de répondre **sans hésiter** à ces questions :

* Pourquoi ce fichier existe ?
* Pourquoi il est dans cette couche et pas une autre ?
* Qu’est-ce qui se passerait s’il n’existait pas ?
* Qu’est-ce qu’il a le droit de faire ?
* Qu’est-ce qu’il n’a PAS le droit de faire ?

---

# 🧠 1. LE PROBLÈME DE DÉPART (TRÈS IMPORTANT)

Tu développes un système de machine learning.

À un moment, tu te dis :

> « Je veux tracer mes expériences : paramètres, métriques, artefacts. »

Et tu choisis **MLflow**.

⚠️ Problème classique :

Si tu mets MLflow **partout** dans ton code :

* dans le domaine
* dans les use cases
* dans les services

👉 ton système devient **dépendant d’un outil**
👉 ton métier est **pollué par une technologie**
👉 changer MLflow devient **quasi impossible**

👉 **Clean Architecture sert à empêcher ça.**

---

# 🧱 2. LA STRATÉGIE CLEAN ARCHITECTURE

On va séparer le problème en **4 intentions distinctes** :

| Intention                    | Question posée                                         |
| ---------------------------- | ------------------------------------------------------ |
| **Besoin métier**            | *De quoi mon système a-t-il besoin pour fonctionner ?* |
| **Orchestration**            | *Quand et comment j’utilise ce besoin ?*               |
| **Implémentation technique** | *Comment c’est fait concrètement ?*                    |
| **Configuration technique**  | *Comment je configure l’outil ?*                       |

👉 Chaque intention = **une couche**.

---

# 🟦 3. DOMAIN — LE BESOIN (LE PLUS IMPORTANT)

## 📁 `domain/ports/experiment_tracking_port.py`

### 🧠 Question à laquelle ce fichier répond

> **« De quoi le cœur de mon système a-t-il besoin ? »**

Réponse :

> « J’ai besoin de pouvoir tracer une expérience ML. »

⚠️ Pas :

* comment
* avec quel outil
* où sont stockés les fichiers

👉 **Juste le besoin.**

---

### 🎯 Rôle pédagogique

Ce fichier :

* **protège le domaine**
* **empêche MLflow d’entrer**
* **force l’infrastructure à s’adapter au métier**

C’est un **contrat**.

---

### 🧩 Analogie simple

Imagine un interrupteur :

* Le domaine dit :
  👉 « J’ai besoin d’un interrupteur ON/OFF »
* Il ne dit PAS :

  * quelle marque
  * quelle tension
  * quel câble

👉 L’électricité (MLflow) s’adapte à l’interrupteur, pas l’inverse.

---

### 🚫 Ce qu’il n’a PAS le droit de faire

* ❌ importer MLflow
* ❌ lire des variables d’environnement
* ❌ écrire des fichiers
* ❌ logger techniquement

---

# 🟩 4. APPLICATION — L’ORCHESTRATION (LE QUAND)

## 📁 `application/services/experiment_tracking_service.py`

> *(Optionnel, mais très propre — exactement comme tu l’as dit)*

---

### 🧠 Question à laquelle ce fichier répond

> **« Quand et comment j’utilise le tracking ? »**

Exemples :

* Quand démarre une expérience ?
* Qu’est-ce que je log au début ?
* Qu’est-ce que je log à la fin ?

👉 Ce n’est PAS du métier.
👉 Ce n’est PAS de la technique.

👉 C’est de **l’orchestration**.

---

### 🎯 Pourquoi ce fichier est optionnel

Tu pourrais faire :

```python
use_case:
    tracker.setup_experiment(...)
    tracker.start_run(...)
    tracker.log_params(...)
```

Mais :

* ce serait répété partout
* ce serait difficile à faire évoluer
* ce serait moins lisible

👉 Le service **centralise les conventions**.

---

### 🧩 Analogie simple

Le domaine dit :

> « J’ai besoin d’un suivi. »

L’application dit :

> « Voilà COMMENT on suit une expérience chez nous. »

---

### 🚫 Ce qu’il n’a PAS le droit de faire

* ❌ importer MLflow
* ❌ lire `os.environ`
* ❌ décider où sont stockés les artefacts

---

# 🟨 5. INFRASTRUCTURE — L’IMPLÉMENTATION TECHNIQUE

## 📁 `infrastructure/tracking/mlflow_adapter.py`

---

### 🧠 Question à laquelle ce fichier répond

> **« Comment je fais concrètement ce tracking ? »**

Réponse :

> « Avec MLflow. »

👉 **Ici seulement**, MLflow est autorisé.

---

### 🎯 Rôle pédagogique

Ce fichier :

* implémente le contrat du domaine
* traduit :

  * `log_metrics()` → `mlflow.log_metrics()`
  * `start_run()` → `mlflow.start_run()`
* isole MLflow du reste du système

👉 C’est un **adaptateur**.

---

### 🧩 Analogie simple

Le domaine parle **français**
MLflow parle **anglais**

👉 L’adapter est le **traducteur**

---

### 🚫 Ce qu’il n’a PAS le droit de faire

* ❌ décider quand tracer (c’est l’application)
* ❌ contenir de logique métier
* ❌ contenir des règles fonctionnelles

---

# 🟥 6. INFRASTRUCTURE — LA CONFIGURATION TECHNIQUE

## 📁 `infrastructure/tracking/mlflow_setup.py`

---

### 🧠 Question à laquelle ce fichier répond

> **« Comment je configure MLflow sur cette machine / environnement ? »**

Exemples :

* Tracking URI
* Artifact URI
* Client MLflow

👉 Ce sont des **détails système**.

---

### 🎯 Pourquoi ce fichier doit être séparé

Parce que :

* la configuration peut changer
* les environnements peuvent changer
* MLflow peut être remplacé

👉 On isole tout ce qui est :

* `os.environ`
* chemins
* URIs
* clients

---

### 🧩 Analogie simple

C’est comme :

* configurer une base de données
* configurer un serveur
* configurer une API externe

👉 Ce n’est **pas** du métier.

---

### 🚫 Ce qu’il n’a PAS le droit de faire

* ❌ décider du nom de l’expérience
* ❌ lancer une run
* ❌ logger des métriques

---

# 🧠 7. COMMENT TOUT ÇA COLLABORE (FIL COMPLET)

```
Use Case
   |
   v
ExperimentTrackingService   ← orchestration
   |
   v
ExperimentTrackingPort      ← contrat
   |
   v
MLflowTrackingAdapter       ← implémentation
   |
   v
MLflow (lib externe)
```

Et à côté :

```
MLflowConfigurator → configure MLflow
```

---

# 🏁 CONCLUSION À RETENIR (TRÈS IMPORTANT)

| Élément                   | Rôle                 |
| ------------------------- | -------------------- |
| **Port (domain)**         | Définit le besoin    |
| **Service (application)** | Ordonne l’usage      |
| **Adapter (infra)**       | Implémente la techno |
| **Setup (infra)**         | Configure la techno  |

👉 Le domaine **ne dépend de rien**
👉 L’infrastructure **dépend du domaine**
👉 MLflow est **remplaçable**
👉 Ton architecture est **propre et professionnelle**

---

Si tu veux, prochaine étape :

* 🔥 diagramme visuel
* 🔥 exercice pratique (on enlève MLflow et on met un FakeTracker)
* 🔥 comparaison avec une architecture “sale”
* 🔥 quand NE PAS appliquer ce niveau de découpage

Dis-moi 👌
