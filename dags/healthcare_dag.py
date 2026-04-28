from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

from scripts.generate import generate_data
from scripts.validate import validate_data
from scripts.classify import classify_data
from scripts.load import load_data

with DAG(
    dag_id="healthcare_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False
) as dag:

    t1 = PythonOperator(
        task_id="generate_data",
        python_callable=generate_data,
        retries=2
    )

    t2 = PythonOperator(
        task_id="validate_data",
        python_callable=validate_data,
        retries=2
    )

    t3 = PythonOperator(
        task_id="classify_data",
        python_callable=classify_data,
        retries=2
    )

    t4 = PythonOperator(
        task_id="load_data",
        python_callable=load_data,
        retries=2
    )

    t1 >> t2 >> t3 >> t4