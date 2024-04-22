FROM apache/airflow:latest


USER root

RUN apt-get update && \
    apt-get -y install git && \
    apt-get clean

# Create the docker group
RUN groupadd -g 999 docker

# Add the airflow user to the docker group
RUN usermod -aG docker airflow

# Switch to the new user
USER airflow


RUN pip install apache-airflow-providers-docker
RUN pip install docker
