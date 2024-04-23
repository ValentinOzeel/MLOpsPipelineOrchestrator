import os
from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount
from pathlib import Path
import yaml


# Access Airflow configuration
airflow_config_path = r'/opt/airflow/conf/airflowconfig.yml'
with open(airflow_config_path, 'r') as yaml_file:
    yaml_file = yaml.safe_load(yaml_file)
airflow_config = yaml_file['AIRFLOW_CONFIG']

# Mount data 
container_data_path = airflow_config['container_data_path']
data_path = os.environ.get('DATA_PATH')
mount_data_dir = Mount(target=container_data_path, source=data_path, type='bind')
# Mount Mlflow tracker (mlruns params and tags)
container_mlruns_path = airflow_config['container_mlruns_path']
mlruns_path = os.environ.get('MLRUNS_PATH')
mount_mlruns_dir = Mount(target=container_mlruns_path, source=mlruns_path, type='bind')
# Mount Mlflow tracker (mlruns artifacts)
mlruns_in_docker = os.environ.get('ARTIFACTS_DOCKER_PATH')
mount_artifacts = Mount(target=mlruns_in_docker, source=mlruns_path, type='bind')


pipeline_name, project_image = airflow_config['pipeline_name'], airflow_config['project_image']
user, task_id = airflow_config['user'], airflow_config['task_id']
volumes = [mount_mlruns_dir, mount_data_dir, mount_artifacts]

with DAG(
    dag_id='kedrospaceship',
    default_args={
        'owner': 'airflow',
        'start_date': datetime(airflow_config['start_year'], 
                               airflow_config['start_month'], 
                               airflow_config['start_day']),
        'depends_on_past':False,
        'email_on_failure':False,
        'email_on_retry':False,
        'retries':1,
        'retry_delay':timedelta(minutes=5),
        },
    schedule_interval=airflow_config['schedule_interval'],
) as dag:
    tasks = {
        "create-data-pipelines-node": DockerOperator(
            task_id=task_id,
            image=project_image,
            user=user,
            mounts=volumes,
            mount_tmp_dir=False,
            port_bindings={5000: 5000},
            network_mode ='bridge',
            auto_remove=False,
            docker_url='unix://var/run/docker.sock',
        #    api_version='auto', 
        ),
    }

