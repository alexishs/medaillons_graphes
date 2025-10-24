# medaillons_graphes

## Méthode abordée :

Développement effectué en un projet Python pouvant être lancé via :

- Airflow (DAGs configurés dans dags/medaillons.py)
- CLI/Debug, en dehors de Airflow (depuis dags/main.py)

**La génération des fichiers CSV de test nescessaires sont générés via un lancement en CLI/Debug uniquement.**

## Le brief a été suivi jusqu'à la partie Gold (insertion des noeuds en base, pas eu le temps de gérer les relations).

## Pré-requis
**Ce projet a été développé sous Linux (Ubuntu 24.04 LTS). Les instructions présentées ci-après supposent une installation sous cet environnement.**
Un environnement Docker doit être installé.

## Structure

```bash
 ├── .env.dev.exemple # Modèle de .env.dev à créer
 ├── .gitignore
 ├── .vscode
 │  └── launch.json # Permet de debuggage directement dans vscode
 ├── airflow_dev.Dockerfile
 ├── config_pgadmin_dev.json.exemple # Exemple de fichier config_pgadmin_dev.json à créer pour la configuration automatique de l'interface d'administration du metastore d'Airflow (optionnel)
 ├── creer_demarrer_conteneurs_dev.sh # Crée et démmarre les conteneurs Docker
 ├── dags # projet Python (répertoire de travail pour exécution via CLI)
 │  ├── .airflowignore
 │  ├── .gitkeep
 │  ├── main.py # Point d'entrée pour CLI/Debug
 │  ├── medaillons.py # Configuration des DAGs d'Airflow
 │  └── metier # Répertoire contenant le code métier
 ├── data # Stockage des fichiers CSV et Parquet générés
 │  ├── .gitkeep
 │  ├── bronze
 │  ├── donnees_brutes
 │  ├── gold
 │  └── silver
 ├── docker_compose_dev.yaml
 ├── generer_cles_secretes.py # Pour la configuration Airflow
 ├── lister_bibliotheques_python.sh # Permet de lister les bibliothèques utilisées par Airflow
 ├── logs_airflow
 ├── README.md
 ├── requirements.txt # Bibliothèques Python générée à partir de la configuration utilisée par Airflow
 ├── supprimer_conteneurs_dev.sh # Supprime les conteneurs Docker
 └── tout_reinitialiser.sh # Supprime et recrée et lance les conteneurs Docker en supprimmant les images et volumes non utilisés
```

## Configuration

### Fichier .env.dev
Créer un fichier .env.dev en se basant sur le fichier .env.dev.exemple

### Fichier config_pgadmin_dev.json
*Etape optionnelle permettant de se connecter au metastore de airflow.*
Fichier à créer pour la configuration du service PGAdmin.
Les valeurs pour Username et MaintenanceDB doivent correspondre aux variables POSTGRES_USER et POSTGRES_DB.
Le mot de passe correspond à la valeur de la variable POSTGRES_PASSWORD.

```json
{
    "Servers": {
        "1": {
            "Name": "PostgreSQL Service",
            "Group": "Docker Servers",
            "Port": 5432,
            "Username": "mettre la même valeur que la variable POSTGRES_USER",
            "Host": "airflow_postgres_dev",
            "SSLMode": "prefer",
            "MaintenanceDB": "mettre la même valeur que la variable POSTGRES_DB"
        }
    }
}
```

## Installation des services Airflow/Neo4J avec Docker

```bash
creer_demmarrer_conteneurs_dev.sh
```

Liste des ports par services créés et accessibles en HTTP :

- 8080 : Console d'administration d'Airflow avec ses DAGs ;
- 8081 : PGAdmin (si besoin d'accès au Metastore d'Airflow)
- 7474 : Neo4J

Autre port ouvert : 7687 (requêtes Cypher pour Neo4J)

## Exécution en local/Débogage

Il est possible d'exécuter/déboger en local le code métier.

Le développement est effectué dans le dossier "dags".

### Création de l'environnement virtuel :

```bash
# on crée le répertoire caché de l'environnement (avec utilisation du module venv)
python -m venv .venv
# on active l'environnement
source .venv/bin/activate
# Installation des librairies nécessaire pour une exécution locale en dehors d'Airflow
pip install -r requirements.txt
```

Le fichier requirements.txt a été généré à partir des versions exactes des bibliothèques utilisées par Airflow dans ses conteneurs Docker afin de pouvoir exécuter/debugger en local avec la même configuration que Airflow.
Il est possible de lister les bibliothèques installées dans les conteneurs avec le script lister_bibliotheques_pyton.sh

En cas d'évolution de la configuration de Airflow, le fichier requirements.txt peut être actualisé avec cette commande :

```bash
./lister_bibliotheques_pyton.sh > requirements.txt
```

### Exécution en CLI (sans Airflow)

```bash
# on se déplace dans le sous-dossier dags
cd ./dags
python main.py
```

**Bien que l'exécution manuelle ne néscessite pas Airflow, les services conteneurisés doivent tourner (utilisation de Neo4J)**

### Débogage dans VSCode

Le fichier .vscode/launch.json inclus permet de déboger l'ensemble du code Python dans vscode.

## Observations diverses sur le développement

### Différentes méthodes testées pour l'import dans Neo4J.

- par Cypher depuis Python sans fichiers CSV (bien trop lours)
- en exposant les fichiers CSV d'import (partie Gold) dans Neo4J puis en effectuant, en python une requête Cypher avec LOAD CSV…
- l'import via neo4j-admin n'a pas été testé (pas eu le temps).

*Note : même avec un fichier CSV et la requête LOAD CSV, l'import est très lourd et il a fallu drastiquement diminuer le nombre de noeuds (cf. dags/main.py) pour que le code puisse être testé convenablement (pas d'erreur constatée, mais bien trop long avec 1M de noeuds…).*

### CLI/Makefile

Pas eu le temps de faire un makefile, mais le code permet de le créer façilement.

Pour cela, il faut gérer les arguments de la ligne de commande dans main.py (avec argparse) puis créer un makefile en appellant les arguments idoines en fonction de l'étape à exécuter.

Dans la pratique, le code a été développé avec le debugger depuis vscode en activant/commentant les étapes désirées directement depuis main.py.

### Airflow

Toutes les fonctionnalités disponibles en CLI/Debug sont disponibles depuis Airflow.

Seule la création des fichiers CSV de test est uniquement faite depuis dags/main.py (ce fichier n'étant pas utilisé par Airflow).

Il n'y a pas de déclenchement automatique dans Airflow (si besoin, un commentaire dans la configuration des DAGs explique comment configurer le déclenchement automatique).

### Autres remarques

- Pas eu le temps de correctement logger l'avancée du pipeline (j'aurais dû le faire au fur et à mesure…), bien que les erreurs soient remontées.
- Pas eu le temps non plus de générer les docstrings.

J'arrête là.