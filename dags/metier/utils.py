from __future__ import annotations
import os
from dotenv import load_dotenv
from pathlib import Path
import shutil
import pandas

REPERTOIRE_DONNEES_BRUTES = 'data/donnees_brutes'
REPERTOIRE_BRONZE = 'data/bronze'
REPERTOIRE_SILVER = 'data/silver'
REPERTOIRE_GOLD = 'data/gold'

def definir_en_test()-> None:
    os.environ['TEST'] = str(True)
    load_dotenv("../.env.dev")

def en_test() -> bool:
    return os.getenv("TEST") == str(True)

def chemin_base(chemin_contenu: str)-> str:
    if en_test():
        return "../" + chemin_contenu
    else:
        return "/opt/airflow/" + chemin_contenu

def initialiser_repertoire(chemin_repertoire: str, avec_suppression: bool = False)-> None:
    chemin_utilise = chemin_base(chemin_repertoire)
    if avec_suppression and os.path.exists(chemin_utilise):
        shutil.rmtree(chemin_utilise)
    Path.mkdir(Path(chemin_utilise), parents=True, exist_ok=True)

def initialiser_repertoires():
    initialiser_repertoire(REPERTOIRE_DONNEES_BRUTES)
    initialiser_repertoire(REPERTOIRE_BRONZE, True)
    initialiser_repertoire(REPERTOIRE_SILVER, True)
    initialiser_repertoire(REPERTOIRE_GOLD, True)

def conversion_csv_vers_parquet(fichier_csv_source: str, fichier_parquet_destination: str)-> None:
    df = pandas.read_csv(fichier_csv_source)
    df.to_parquet(fichier_parquet_destination)