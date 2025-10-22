import pandas
from metier import utils

def conversion_csv_vers_parquet(fichier_csv_source: str, fichier_parquet_destination: str)-> None:
    df = pandas.read_csv(fichier_csv_source)
    df.to_parquet(fichier_parquet_destination)

def convertire_donnees_brutes_vers_bronze()-> None:
    conversion_csv_vers_parquet(
        utils.chemin_base(f"{utils.REPERTOIRE_DONNEES_BRUTES}/noeuds.csv"),
        utils.chemin_base(f"{utils.REPERTOIRE_BRONZE}/noeuds.parq")
    )
    conversion_csv_vers_parquet(
        utils.chemin_base(f"{utils.REPERTOIRE_DONNEES_BRUTES}/relations.csv"),
        utils.chemin_base(f"{utils.REPERTOIRE_BRONZE}/relations.parq")
    )