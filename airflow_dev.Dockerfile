FROM apache/airflow:2.10.2-python3.9

ARG AIRFLOW_UID=50000

USER root
RUN usermod -u "$AIRFLOW_UID" -g 0 airflow && chown "$AIRFLOW_UID":0 -R /home/airflow && chown "$AIRFLOW_UID":0 -R /opt/airflow

USER airflow
RUN pip install --no-cache-dir pyspark pandas fastparquet dotenv great_expectations