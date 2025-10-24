from __future__ import annotations
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime #, timedelta
from metier import utils
from metier.bronze import traitement_bronze
from metier.silver import traitement_silver

default_args = {
    "owner": "airflow",
    "retries": 1,
    #'retry_delay': timedelta(minutes=1),
}

def initialisation()-> None:
    utils.creer_repertoires()

def traitement_gold()-> None:
    pass

with DAG(
    dag_id="gestion_medaillons",
    default_args=default_args,
    description="Gestion des données statiques",
    # mode manuel schedule_interval=timedelta(days=15),
    start_date=datetime(2024, 6, 1),
    catchup=False
) as dag:
    run_initialisation = PythonOperator(
        task_id="run_initialisation",
        python_callable=initialisation
    )
    run_bronze = PythonOperator(
        task_id="run_bronze",
        python_callable=traitement_bronze
    )
    run_silver = PythonOperator(
        task_id="run_silver",
        python_callable=traitement_silver
    )
    run_gold = PythonOperator(
        task_id="run_gold",
        python_callable=traitement_gold
    )

    run_initialisation >> run_bronze >> run_silver >> run_gold