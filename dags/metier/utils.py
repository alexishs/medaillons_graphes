from __future__ import annotations
import os
from dotenv import load_dotenv

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

# def chemin_dags(chemin_contenu: str)-> str:
#     if en_test():
#         return "./" + chemin_contenu
#     else:
#         return "/opt/airflow/dags/" + chemin_contenu