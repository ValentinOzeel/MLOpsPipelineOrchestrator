ARG BASE_IMAGE=python:3.11-slim
FROM $BASE_IMAGE as runtime-environment

# Install Git
RUN apt-get update && apt-get install -y git

COPY /MLp /home/kedro_docker/MLp
# install project requirements
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache -r /tmp/requirements.txt && rm -f /tmp/requirements.txt


# add kedro user
ARG KEDRO_UID=999
ARG KEDRO_GID=0
RUN groupadd -f -g ${KEDRO_GID} kedro_group && \
useradd -m -d /home/kedro_docker -s /bin/bash -g ${KEDRO_GID} -u ${KEDRO_UID} kedro_docker

WORKDIR /home/kedro_docker
USER kedro_docker

FROM runtime-environment

# copy the whole project except what is in .dockerignore
ARG KEDRO_UID=999
ARG KEDRO_GID=0
COPY --chown=${KEDRO_UID}:${KEDRO_GID} . .

EXPOSE 5000

CMD mlflow ui --host=0.0.0.0 --port=5000 & kedro run --pipeline=training --async

