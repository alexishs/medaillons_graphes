import math
from pathlib import Path
import great_expectations as gx
import pandas
from metier import utils

def traitement_silver()-> None:

    def effectuer_tests(df: pandas.DataFrame, liste_tests: list)-> None:
        context = gx.get_context()
        data_source = context.data_sources.add_pandas("pandas")
        data_asset = data_source.add_dataframe_asset(name="pd dataframe asset")
        batch_definition = data_asset.add_batch_definition_whole_dataframe("batch definition")
        batch = batch_definition.get_batch(batch_parameters={"dataframe": df})
        suite = context.suites.add(gx.ExpectationSuite(name="my_exp_suite"))
        for expectation in liste_tests:
            suite.add_expectation(expectation)
        validation_result = batch.validate(suite)
        assert validation_result.success, validation_result

    def partitioner_df_en_fichiers_parquets(df: pandas.DataFrame, chemin_destination_base: str, nom_repertoire_partition: str, nb_partitions: int, nom_fichier: str)-> None:
        taille_df = len(df)
        nb_enreg_partition = math.ceil(taille_df / nb_partitions)
        indice_partition = 0
        indice_debut = 0
        while (indice_debut < (taille_df - 1)):
            indice_fin = indice_debut + nb_enreg_partition
            df_partition = df.iloc[indice_debut:indice_fin]
            repertoire_fichier = f"{chemin_destination_base}/{nom_repertoire_partition}_{indice_partition}"
            Path.mkdir(Path(repertoire_fichier), parents=True, exist_ok=True)
            df_partition.to_parquet(f"{repertoire_fichier}/{nom_fichier}")
            indice_debut = indice_fin + 1
            indice_partition += 1

    # Vérification des données
    df_noeuds = pandas.read_parquet(utils.chemin_base(f"{utils.REPERTOIRE_BRONZE}/noeuds.parq"))
    effectuer_tests(
        df_noeuds,
        [
            gx.expectations.ExpectColumnValuesToBeUnique(column="id_noeud")
        ]
    )
    df_relations = pandas.read_parquet(utils.chemin_base(f"{utils.REPERTOIRE_BRONZE}/relations.parq"))
    effectuer_tests(
        df_relations,
        [
            gx.expectations.ExpectColumnValuesToNotBeNull(column="id_noeud_a"),
            gx.expectations.ExpectColumnValuesToNotBeNull(column="id_noeud_b")
        ]
    )

    # Enregistrement

    # # On pourrait partitionner les noeuds comme pour les arrêtes, mais ce n'est pas demandé.
    # partitioner_df_en_fichiers_parquets(
    #     df_noeuds,
    #     utils.chemin_base(utils.REPERTOIRE_BRONZE),
    #     'partition',
    #     8,
    #     'noeuds.parq'
    # )
    df_noeuds.to_parquet(f"{utils.chemin_base(utils.REPERTOIRE_SILVER)}/noeuds.parq")

    partitioner_df_en_fichiers_parquets(
        df_relations,
        f"{utils.chemin_base(utils.REPERTOIRE_SILVER)}/relations",
        'partition=',
        8,
        'relations.parq'
    )