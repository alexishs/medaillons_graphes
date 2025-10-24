from __future__ import annotations
import os
from dotenv import load_dotenv
from pathlib import Path
import pandas

REPERTOIRE_DONNEES_BRUTES = 'data/donnees_brutes'
REPERTOIRE_BRONZE = 'data/bronze'
REPERTOIRE_SILVER = 'data/silver'

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
    
def creer_chemin_base(chemin_repertoire: str)-> None:
    Path.mkdir(Path(chemin_base(chemin_repertoire)), parents=True, exist_ok=True)

def creer_repertoires():
    creer_chemin_base(REPERTOIRE_DONNEES_BRUTES)
    creer_chemin_base(REPERTOIRE_BRONZE)
    creer_chemin_base(REPERTOIRE_SILVER)

def conversion_csv_vers_parquet(fichier_csv_source: str, fichier_parquet_destination: str)-> None:
    df = pandas.read_csv(fichier_csv_source)
    df.to_parquet(fichier_parquet_destination)