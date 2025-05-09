from airflow.decorators import dag, task
from airflow.hooks.base import BaseHook
from datetime import datetime
import requests
import pandas as pd
from sqlalchemy import create_engine


@dag(
    dag_id="elt_IBGE",
    description="DAG com processamento e carga de dados do IBGE",
    start_date=datetime(2025, 4, 21),
    schedule_interval=None, 
    catchup=False,
    tags=["ibge", "elt", "pandas"]
)
def pipeline_ibge():

    @task
    def extrair_dados():
        url_template = 'https://servicodados.ibge.gov.br/api/v1/paises/{pais}/indicadores/{indicador}'

        paises = ["AR", "BR"]
        indicadores = [
            "77818", "77819", "77820", "77821", "77822", "77823", "77824", "77825",
            "77826", "77829", "77827", "77830", "77831", "77832", "77833", "77834",
            "77835", "77836", "77838", "77839", "77840", "77841", "77842", "77844",
            "77845", "77846", "77847", "77848", "77849", "77850", "77851", "77852",
            "77854", "77855", "77857"
        ]

        dados_por_pais = {}

        for pais in paises:
            dados_por_pais[pais] = {} 

            for indicador in indicadores:
                url = url_template.format(pais=pais, indicador=indicador)
                response = requests.get(url)

                if response.status_code == 200:
                    try:
                        dados = response.json()
                        nome_indicador = dados[0]['indicador']
                        serie = dados[0]['series'][0]['serie']
                        dados_por_pais[pais][nome_indicador] = serie
                    except (KeyError, IndexError, ValueError):
                        print(f"Erro ao processar indicador {indicador} para o país {pais}")
                else:
                    print(f"Erro na requisição para {url} - Status: {response.status_code}")

        return dados_por_pais

    @task
    def processar_dados_ibge(dados_por_pais: dict):
        linhas = []

        for pais, indicadores in dados_por_pais.items():
            for indicador, series in indicadores.items():
                for entrada in series:
                    for ano, valor in entrada.items():
                        linhas.append({
                            "pais": pais,
                            "ano": ano,
                            indicador: valor
                        })

        # Cria DataFrame com dados empilhados
        df_raw = pd.DataFrame(linhas)

        # Agrupa por país e ano, combinando os diferentes indicadores em colunas
        df_final = df_raw.groupby(['pais', 'ano']).first().reset_index()
        return df_final

    @task
    def salvar_dados_em_tabela(df_final: pd.DataFrame):
        conn = BaseHook.get_connection('meu_postgres')
        conn_str = f'postgresql+psycopg2://{conn.login}:{conn.password}@{conn.host}:{conn.port}/{conn.schema}'
        engine = create_engine(conn_str)

        df_final.to_sql('ibge', engine, if_exists='fail', index=False)

    extrair = extrair_dados()
    processar = processar_dados_ibge(extrair)
    salvar = salvar_dados_em_tabela(processar)
    extrair >> processar >> salvar


pipeline_ibge = pipeline_ibge()