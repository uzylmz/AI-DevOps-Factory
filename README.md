# AI DevOps Factory

Plateforme **multi-agents** (Python) qui analyse un dépôt existant, évalue sa maturité DevOps (assets présents/manquants), génère un **rapport**, une **roadmap**, puis peut **générer automatiquement** les assets DevOps manquants (README, .gitignore, Dockerfile, docker-compose, pipeline CI/CD).

> Interface principale : application **Streamlit** (`ui/app.py`).

---

## Sommaire

- [Fonctionnalités](#fonctionnalités)
- [Architecture (vue d’ensemble)](#architecture-vue-densemble)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Configuration (.env)](#configuration-env)
- [Lancer l’application](#lancer-lapplication)
  - [UI Streamlit](#ui-streamlit)
  - [Mode script (orchestrator)](#mode-script-orchestrator)
- [Guide d’utilisation (pas à pas)](#guide-dutilisation-pas-à-pas)
- [Détails des modules / “fonctions” principales](#détails-des-modules--fonctions-principales)
  - [Analyse du dépôt et ProjectSpec](#analyse-du-dépôt-et-projectspec)
  - [Détection des assets DevOps existants](#détection-des-assets-devops-existants)
  - [Analyse des gaps DevOps](#analyse-des-gaps-devops)
  - [Score & niveau de maturité](#score--niveau-de-maturité)
  - [Génération du rapport d’évaluation](#génération-du-rapport-dévaluation)
  - [Génération de la roadmap](#génération-de-la-roadmap)
  - [Génération des assets DevOps manquants](#génération-des-assets-devops-manquants)
  - [Providers LLM (LM Studio / OpenRouter / Azure OpenAI)](#providers-llm-lm-studio--openrouter--azure-openai)
- [Structure du projet](#structure-du-projet)
- [Dépannage](#dépannage)
- [Sécurité / bonnes pratiques](#sécurité--bonnes-pratiques)

---

## Fonctionnalités

- **Analyse d’un projet existant** (chemin local) : détection du langage, framework, base de données, outil de build.
- **Détection des assets DevOps** présents :
  - `README.md`, `.gitignore`
  - `Dockerfile`, `docker-compose.yml` / `compose.yml`
  - Pipelines : Azure DevOps, GitHub Actions, Jenkins, GitLab CI
  - Dossiers Kubernetes (`kubernetes/`, `k8s/`, `helm/`, `charts/`)
  - Fichiers Terraform (`*.tf`)
- **Analyse des manques (gaps)** selon :
  - la plateforme CI/CD cible (Azure DevOps / GitHub Actions / Jenkins / GitLab CI)
  - la méthode de livraison (source code vs container image)
- **Score de maturité DevOps** (0–100) + niveau (Beginner/Basic/Intermediate/Advanced)
- **Rapport d’évaluation** (texte) + **roadmap** priorisée
- **Génération automatique** des assets manquants dans le dépôt analysé :
  - `README.md`, `.gitignore`
  - `Dockerfile`, `docker-compose.yml` (si livraison “container image”)
  - pipeline CI/CD (selon plateforme choisie)

---

## Architecture (vue d’ensemble)

1. **UI Streamlit** (`ui/app.py`) :
   - récupère le chemin du projet
   - permet de choisir la plateforme CI/CD et la méthode de livraison
   - lance l’analyse, affiche score/rapport/roadmap
   - déclenche la génération des assets manquants

2. **Services** :
   - `services/project_spec_builder.py` : construit un `ProjectSpec` à partir du dépôt
   - `services/devops_gap_service.py` : produit un `gap_report` (assets + gaps)
   - `services/devops_assessment.py` : calcule score + maturité
   - `services/report_generator.py` : génère le rapport d’évaluation
   - `services/roadmap_generator.py` + `services/roadmap_report_generator.py`

3. **Agents** :
   - `agents/repository_analyzer_agent/*` : analyse du dépôt (LLM + heuristiques) et détection assets
   - `agents/devops_agent/agent.py` : génération des fichiers DevOps (Dockerfile, pipeline, etc.)
   - `agents/lead_agent/agent.py` : orchestration de la génération
   - `agents/documentation_agent/agent.py` : génération de docs (dans `generated_projects/...`)

4. **LLM** :
   - `services/llm_service.py` route vers un provider (LM Studio par défaut, OpenRouter optionnel)

---

## Prérequis

- **Python 3.11+** (recommandé)
- (Optionnel) **LM Studio** si vous utilisez le provider local (par défaut)
- (Optionnel) une clé **OpenRouter** si vous utilisez OpenRouter
- (Optionnel) accès **Azure OpenAI** si vous utilisez Azure (provider présent mais non branché par défaut)

---

## Installation

```bash
python -m venv .venv

# Windows PowerShell
.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

---

## Configuration (.env)

Créez un fichier `.env` à la racine (ou exportez les variables) selon le provider LLM.

### Option A — LM Studio (par défaut)
Aucune variable obligatoire.

- L’app appelle un endpoint compatible OpenAI : `http://localhost:1234/v1`
- Modèle utilisé dans le code : `qwen` (voir `services/lmstudio_provider.py`)

### Option B — OpenRouter
Définir :

- `LLM_PROVIDER=openrouter`
- `OPENROUTER_API_KEY=...`
- `OPENROUTER_MODEL=...` (ex: `openai/gpt-4o-mini`, `anthropic/claude-3.5-sonnet`, etc.)

### Option C — Azure OpenAI (présent)
Le provider existe (`services/azure_provider.py`) mais **n’est pas sélectionné** par `services/llm_service.py` actuellement.

Variables attendues :

- `AZURE_OPENAI_API_KEY=...`
- `AZURE_OPENAI_ENDPOINT=...`
- `AZURE_OPENAI_API_VERSION=...`
- `AZURE_OPENAI_DEPLOYMENT=...`

---

## Lancer l’application

### UI Streamlit

```bash
streamlit run ui/app.py
```

Ensuite, ouvrez l’URL affichée par Streamlit.

### Mode script (orchestrator)

Le fichier `orchestrator/main.py` est un exemple de pipeline “script” (non interactif) qui :
- analyse un projet
- calcule gaps
- génère rapport + roadmap + executive summary
- génère les assets manquants

```bash
python orchestrator/main.py
```

> Note : `orchestrator/main.py` contient un `project_path` en dur (Windows). Modifiez-le avant exécution.

---

## Guide d’utilisation (pas à pas)

1. Lancez l’UI Streamlit.
2. Dans la sidebar :
   - choisissez la **plateforme CI/CD** cible (Azure DevOps / GitHub Actions / Jenkins / GitLab CI)
   - choisissez la **méthode de livraison** :
     - **Source Code** : pas d’exigence Docker
     - **Container Image** : Dockerfile + docker-compose deviennent requis
3. Saisissez le **chemin absolu** du projet à analyser.
4. Cliquez **Analyze project**.
5. Consultez :
   - plateforme détectée (si existante)
   - infos projet (langage/framework/build tool)
   - score + maturité
   - assets présents/manquants
   - roadmap
   - rapport complet
6. Cliquez **Generate missing assets** pour écrire les fichiers manquants **directement dans le dépôt analysé**.

---

## Détails des modules / “fonctions” principales

### Analyse du dépôt et ProjectSpec

- **Modèle** : `models/project_spec.py` → `ProjectSpec` (Pydantic)
- **Construction** : `services/project_spec_builder.py` → `build_project_spec_from_repository(project_path)`

Processus :
1. `agents/repository_analyzer_agent/agent.py` construit un contexte (extraits de fichiers clés) et appelle le LLM.
2. Le LLM retourne un JSON : `language`, `framework`, `database`, `build_tool`.
3. `existing_devops_detector.detect_existing_devops_assets()` détecte les assets DevOps.
4. Un `ProjectSpec` est instancié.

> Remarque : le `project_name` est actuellement dérivé de `language` (`"{language}-project"`).

### Détection des assets DevOps existants

- `agents/repository_analyzer_agent/existing_devops_detector.py`

Détecte notamment :
- `README.md`, `.gitignore`
- `Dockerfile`
- `docker-compose.yml` / `compose.yml` (et variantes `.yaml`)
- Pipelines :
  - Azure DevOps : `azure-pipelines.yml|yaml`
  - GitHub Actions : présence de `.github/workflows/*.yml|yaml`
  - Jenkins : `Jenkinsfile`
  - GitLab CI : `.gitlab-ci.yml`
- Kubernetes : dossiers `kubernetes/`, `k8s/`, `helm/`, `charts/`
- Terraform : fichiers `*.tf`

Le résultat inclut aussi `ci_cd_platforms` (liste des plateformes détectées).

### Analyse des gaps DevOps

- `agents/repository_analyzer_agent/gap_analyzer.py` → `analyze_devops_gaps(assets, target_ci_cd_platform, delivery_method)`
- `services/devops_gap_service.py` → `get_devops_gap_report(...)`

Règles principales :
- `generate_pipeline` est vrai si la pipeline de la plateforme **sélectionnée** est absente.
- Si `delivery_method == "container_image"` :
  - `generate_dockerfile` et `generate_docker_compose` deviennent requis.
- `generate_readme` si `README.md` absent.
- `generate_gitignore` si `.gitignore` absent.

### Score & niveau de maturité

- `services/devops_assessment.py`

Score basé sur :
- `.gitignore` (20)
- `README.md` (15)
- pipeline CI/CD (30)
- si livraison container : `Dockerfile` (20) + `docker-compose` (15)

Niveau :
- <25 Beginner
- <50 Basic
- <75 Intermediate
- >=75 Advanced

### Génération du rapport d’évaluation

- `services/report_generator.py` → `generate_devops_report(specification, gap_report)`

Produit un rapport texte :
- infos projet
- assets présents/manquants
- score + maturité
- recommandations (liste)

### Génération de la roadmap

- `services/roadmap_generator.py` → `generate_devops_roadmap(gap_report)`
- `services/roadmap_report_generator.py` → `generate_roadmap_report(roadmap)`

Roadmap priorisée (1..n) selon les gaps.

### Génération des assets DevOps manquants

- Orchestration : `agents/lead_agent/agent.py` → `execute_project_generation(spec, gap_report, target_path)`
- Génération fichiers : `agents/devops_agent/agent.py` → `generate_project_structure(spec, gap_report, target_path)`

Fichiers générés selon les gaps :
- `Dockerfile` (template selon langage : python/java/node/other)
- `docker-compose.yml` (ports selon langage)
- `README.md` (infos projet + plateforme + delivery)
- `.gitignore` (commun + spécifique langage)
- Pipeline CI/CD :
  - Azure DevOps : `azure-pipelines.yml`
  - GitHub Actions : `.github/workflows/ci.yml`
  - Jenkins : `Jenkinsfile`
  - GitLab CI : `.gitlab-ci.yml`

> Important : l’UI prévient que les fichiers sont écrits dans le dépôt analysé. Le code n’implémente pas explicitement une protection “anti-overwrite” autre que le fait de ne générer que si gap=true.

### Providers LLM (LM Studio / OpenRouter / Azure OpenAI)

- Routeur : `services/llm_service.py` → `ask_llm(prompt)`
  - `LLM_PROVIDER=openrouter` → `services/openrouter_provider.py`
  - sinon → `services/lmstudio_provider.py`

- OpenRouter : nécessite `OPENROUTER_API_KEY` + `OPENROUTER_MODEL`
- LM Studio : endpoint local `http://localhost:1234/v1`
- Azure : `services/azure_provider.py` (non branché par défaut)

---

## Structure du projet

```text
.
├─ agents/
│  ├─ architect_agent/
│  ├─ devops_agent/
│  ├─ documentation_agent/
│  ├─ lead_agent/
│  └─ repository_analyzer_agent/
├─ docs/
├─ models/
├─ orchestrator/
│  └─ main.py
├─ services/
├─ templates/
├─ ui/
│  └─ app.py
├─ requirements.txt
└─ README.md
```

---

## Dépannage

### 1) Streamlit ne trouve pas les modules
`ui/app.py` ajoute le `PROJECT_ROOT` au `sys.path`. Si vous lancez depuis un autre dossier, lancez toujours depuis la racine :

```bash
streamlit run ui/app.py
```

### 2) Le LLM ne répond pas / réponse JSON invalide
L’analyse du dépôt via LLM exige un **JSON strict**. En cas d’erreur :
- vérifiez le provider (LM Studio en cours d’exécution ?)
- essayez OpenRouter avec un modèle plus fiable
- regardez la sortie console : `agents/repository_analyzer_agent/agent.py` affiche la réponse brute

### 3) LM Studio
Assurez-vous que LM Studio expose bien un serveur compatible OpenAI sur :
- `http://localhost:1234/v1`

### 4) Génération pipeline GitHub Actions
Le fichier est écrit dans : `.github/workflows/ci.yml`.
Assurez-vous que le dépôt analysé autorise la création de dossiers.

---

## Sécurité / bonnes pratiques

- Ne commitez jamais votre `.env`.
- Les fichiers générés sont des **templates** : adaptez-les à vos standards (tests, lint, build, scan, déploiement, secrets, etc.).
- Avant d’exécuter une pipeline générée, vérifiez :
  - commandes de build/test
  - versions runtime
  - secrets/variables CI

