from __future__ import annotations
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

    # Etape 2 : partitionnement
