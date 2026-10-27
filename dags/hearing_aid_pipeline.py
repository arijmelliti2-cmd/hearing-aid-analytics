
from datetime import timedelta

import pendulum

from airflow import DAG
from airflow.operators.bash import BashOperator


DBT_PROJECT_DIR = "/opt/airflow/dbt_project/hearing_aid_analytics"
DBT_PROFILES_DIR = "/opt/airflow/profiles"
LOCAL_TZ = pendulum.timezone("Europe/Berlin")

default_args = {
    "owner": "data-engineering",
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}


with DAG(
    dag_id="hearing_aid_pipeline",
    description="Orchestrate the hearing-aid analytics dbt pipeline",
    default_args=default_args,
    start_date=pendulum.datetime(2026, 1, 1, tz=LOCAL_TZ),
    schedule="0 6 * * *",
    catchup=False,
    max_active_runs=1,
    dagrun_timeout=timedelta(hours=1),
    tags=["dbt", "postgres", "hearing-aid"],
) as dag:

    seed_data = BashOperator(
        task_id="seed_data",
        bash_command=(
            f"dbt seed "
            f"--project-dir {DBT_PROJECT_DIR} "
            f"--profiles-dir {DBT_PROFILES_DIR}"
        ),
    )

    build_models = BashOperator(
        task_id="build_models",
        bash_command=(
            f"dbt build "
            f"--project-dir {DBT_PROJECT_DIR} "
            f"--profiles-dir {DBT_PROFILES_DIR}"
        ),
    )

    generate_docs = BashOperator(
        task_id="generate_docs",
        bash_command=(
            f"dbt docs generate "
            f"--project-dir {DBT_PROJECT_DIR} "
            f"--profiles-dir {DBT_PROFILES_DIR}"
        ),
    )

    seed_data >> build_models >> generate_docs
