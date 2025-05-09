from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime

default_args = {
    'start_date': datetime(2024, 1, 1)
}

with DAG(dag_id='dag_teste_simples', default_args=default_args, schedule_interval=None, catchup=False) as dag:
    tarefa = DummyOperator(task_id='tarefa_dummy')




with DAG(
    dag_id='exemplo_postgres',
    schedule_interval=None,
    default_args=default_args,
    catchup=False
) as dag:

    criar_tabela = PostgresOperator(
        task_id='criar_tabela_exemplo',
        postgres_conn_id='meu_postgres',
        sql="""
            CREATE TABLE IF NOT EXISTS exemplo (
                id SERIAL PRIMARY KEY,
                nome TEXT
            );
        """
    )
