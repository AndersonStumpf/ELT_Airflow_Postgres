FROM apache/airflow:2.7.1

USER root
RUN pip install pyspark

USER airflow
