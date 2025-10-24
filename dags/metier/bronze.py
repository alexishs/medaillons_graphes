from metier import utils

def traitement_bronze()-> None:
    utils.conversion_csv_vers_parquet(
        utils.chemin_base(f"{utils.REPERTOIRE_DONNEES_BRUTES}/noeuds.csv"),
        utils.chemin_base(f"{utils.REPERTOIRE_BRONZE}/noeuds.parq")
    )
    utils.conversion_csv_vers_parquet(
        utils.chemin_base(f"{utils.REPERTOIRE_DONNEES_BRUTES}/relations.csv"),
        utils.chemin_base(f"{utils.REPERTOIRE_BRONZE}/relations.parq")
    )