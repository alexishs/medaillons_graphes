import pandas
import os
from neo4j import GraphDatabase
from metier import utils

TAILLE_BATCH_NEO4J = 1000

def traitement_gold()-> None:
    """Exportation sur disque et serveur Neo4j en respectant la nomenclature imposée.
    Exportations vers Neo4j uniquement par requête Cypher vers le serveur distant (pas d'accès au FS du serveur)
    sans utiliser d'exportation des fichiers CSV (donc pas de LOAD CSV…)
    """

    # def creer_noeud(transaction, enreg):
    #     # version ajout uniquement
    #     requete = f"""
    #         CREATE (u:User {{id: {enreg['ID']}, name: '{enreg['name']}', label: '{enreg['label']}'}})
    #     """
    #     # version avec gestion des enregs déjà existants
    #     # requete = f"""
    #     #     MERGE (u:User {{id: {enreg['ID']}}})
    #     #     SET u.name = '{enreg['name']}', u.label = '{enreg['label']}'
    #     # """
    #     transaction.run(requete)

    # Traitement des noeuds
    df_noeuds = pandas.read_parquet(f"{utils.chemin_base(utils.REPERTOIRE_SILVER)}/noeuds.parq")
    df_noeuds = df_noeuds.rename(columns={
        'id_noeud': 'id',
        'type_noeud': 'name',
        'nom_noeud': 'label'
    })
    df_noeuds.to_csv(f"{utils.chemin_base(utils.REPERTOIRE_GOLD)}/nodes.csv", index=False)
    df_relations = pandas.read_parquet(f"{utils.chemin_base(utils.REPERTOIRE_SILVER)}/relations")
    df_relations = df_relations.rename(columns={
        'id_noeud_a': ':START_ID',
        'id_noeud_b': ':END_ID'
    })
    df_relations.to_csv(f"{utils.chemin_base(utils.REPERTOIRE_GOLD)}/edges.csv", index=False)

    driver = GraphDatabase.driver('bolt://localhost:7687', auth=("neo4j", "neo4j"))

    # c'est trèèèèèèèèèèèèèèèèèèèèès long avec 1M de noeuds !!!!
    with driver.session() as session:
        chaine_requete = """
        LOAD CSV WITH HEADERS FROM 'file:///gold/nodes.csv' AS row
        MERGE (u:User {id: toInteger(row.id)})
        SET 
            u.name = row.name,
            u.label = row.label;
        """
        session.execute_write(
            lambda tx: tx.run(chaine_requete)
        )
    
    # pas le temps de gérer les relations…

    # Carrément plus long encore ! On enterre définitivement cette méthode !!!
    # =========================================================
    # for indice_debut in range(0, len(df_noeuds), TAILLE_BATCH_NEO4J):
    #     df_batch = df_noeuds.iloc[indice_debut:indice_debut + TAILLE_BATCH_NEO4J]
    #     with driver.session() as session:
    #         for _, row in df_batch.iterrows():
    #             session.execute_write(creer_noeud, row.to_dict())

