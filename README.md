# IBGE Data Pipeline

[![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-017CEE?style=for-the-badge&logo=Apache%20Airflow&logoColor=white)](https://airflow.apache.org/)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

This repository contains an Extract, Load, Transform (ELT) pipeline built with Apache Airflow to collect, process, and store economic and social indicators from countries using the IBGE API (Brazilian Institute of Geography and Statistics).

The pipeline extracts data from multiple indicators, processes it into a structured format, and loads it into a PostgreSQL database for further analysis.

## Features

- **Data Extraction**: Fetches data from the IBGE API for Brazil and Argentina
- **Parallel Processing**: Collects data for 35 different indicators
- **Structured Data**: Organizes data by country and year in a consistent format
- **PostgreSQL Integration**: Stores processed data in a relational database
- **Modular Design**: Uses Airflow's TaskFlow API for clean, maintainable code

## Prerequisites

- Python 3.8+
- Apache Airflow 2.0+
- PostgreSQL database
- Required Python packages:
  - pandas
  - requests
  - sqlalchemy
  - psycopg2

## Installation

1. Clone the repository:
```bash
git clone https://github.com/AndersonStumpf/ELT_Airflow_Postgres.git
cd ibge-data-pipeline
```

2. Install the required packages:
```bash
pip install apache-airflow pandas requests sqlalchemy psycopg2
```

3. Configure Airflow connection for PostgreSQL:
```bash
airflow connections add 'meu_postgres' \
    --conn-type 'postgres' \
    --conn-login 'airflow' \
    --conn-password 'airflow' \
    --conn-host 'postgres' \
    --conn-port 5432 \
```

## Usage

1. Place the DAG file in your Airflow DAGs folder:
```bash
cp elt_ibge.py ~/airflow/dags/
```

2. Start the Airflow webserver and scheduler:
```bash
airflow webserver --port 8080
airflow scheduler
```

3. Access the Airflow UI at http://localhost:8080 and trigger the `elt_IBGE` DAG.

## Pipeline Structure

The pipeline consists of three main tasks:

1. **extrair_dados()**: Extracts data from the IBGE API for specified countries and indicators
2. **processar_dados_ibge()**: Processes and structures the data into a pandas DataFrame
3. **salvar_dados_em_tabela()**: Loads the processed data into a PostgreSQL database

## API Indicators

The pipeline collects data for 35 different indicators (77818-77857) from the IBGE API, which include:

- Economic indicators
- Demographic data
- Social metrics
- Development indices

## Database Schema

The data is stored in a table called `ibge` with the following structure:

- `pais`: Country code (BR, AR)
- `ano`: Year of the data
- Various indicator columns: Each indicator gets its own column with the value for the given country and year

## Customization

You can customize the pipeline by:

- Modifying the list of countries in the `paises` variable
- Adding or removing indicators in the `indicadores` list
- Changing the database table name in the `to_sql` function


## Acknowledgments

- [IBGE](https://www.ibge.gov.br/) for providing the public API
- [Apache Airflow](https://airflow.apache.org/) for the workflow management platform
