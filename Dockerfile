FROM apache/airflow:2.10.5

COPY requirements.txt /opt/airflow/requirements.txt

USER root

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    python3-dev

USER airflow

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /opt/airflow/requirements.txt

ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG AWS_DEFAULT_REGION

ENV AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
ENV AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
ENV AWS_DEFAULT_REGION=${AWS_DEFAULT_REGION}
