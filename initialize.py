import subprocess
import os
import time

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def launch_mlflow_server():
    # Run kedrospaceship training once to initialize mlruns folder (with its meta.yml files)
    mlflow_server_process = subprocess.Popen("mlflow ui", shell=True)
    return mlflow_server_process

def end_process(process):
    process.terminate()

def run_command_blocking(command):
    # Wait for completion of the command before going to the next line of code
    subprocess.run(command, shell=True)
    
    
if __name__ == "__main__":
    
    run_command_blocking(f'cd {os.path.join(root_path, 'kedrospaceship')}')
    # install_package_in_path (kedrospaceship & dependencies) and wait for completion
    run_command_blocking('pip install .')
    # Run kedro mlflow init
    run_command_blocking("kedro mlflow init")
    
    # Run mlflow server
    mlflow_server_process = launch_mlflow_server()
    # Wait for the server to be running
    time.sleep(15)
    # Run kedro pipeline to init mlruns folder (with its meta.yml files)
    run_command_blocking("kedro run --pipeline=training")
    # End mlflow server (going to be ran in docker)
    end_process(mlflow_server_process)

    # Cd to project root
    run_command_blocking(f'cd {root_path}')
    # Create kedrospaceship Docker image
    run_command_blocking("docker build --pull --rm -f 'kedrospaceship\Dockerfile' -t kedrospaceship:latest 'kedrospaceship'") 
    # Create airflow app Docker image
    run_command_blocking("docker build --pull --rm -f 'airflow\Dockerfile' -t airflow_docker:latest 'airflow'")
    # Run docker-compose
    run_command_blocking("docker compose -f 'airflow\docker-compose.yml' up -d --build")