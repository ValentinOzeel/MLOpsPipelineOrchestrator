import subprocess
import os
import time

root_path = os.path.abspath(os.path.dirname(__file__))

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
    # Cd to kedrospaceship dir
    os.chdir(os.path.join(root_path, 'kedrospaceship'))
    # install_package_in_path (kedrospaceship & dependencies) and wait for completion
    print('\n- Installing kedrospaceship and dependencies...'.upper())
    run_command_blocking('pip install .')
    # Run kedro mlflow init
    print('\n- Initializing kedro mlflow...'.upper())
    run_command_blocking("kedro mlflow init")
    
    # Run mlflow server
    print('\n- Launching mlflow server...'.upper())
    mlflow_server_process = launch_mlflow_server()
    # Wait for the server to be running
    time.sleep(15)
    # Run kedro pipeline to init mlruns folder (with its meta.yml files)
    print('\n- Initializing mlflow experiment...'.upper())
    run_command_blocking("kedro run --pipeline=training")
    # End mlflow server (going to be ran in docker)
    print('\n- Closing mlflow server...'.upper())
    end_process(mlflow_server_process)

    # Cd to project root
    os.chdir(root_path)
    # Create kedrospaceship Docker image
    print('\n- Creating kedrospaceship docker image...'.upper())
    run_command_blocking(f"docker build --pull --rm -f {os.path.join(root_path, 'kedrospaceship/Dockerfile')} -t kedrospaceship:latest {os.path.join(root_path, 'kedrospaceship')}") 
    # Create airflow app Docker image
    print('\n- Creating airflow docker image...'.upper())
    run_command_blocking(f"docker build --pull --rm -f {os.path.join(root_path, 'airflow/Dockerfile')} -t airflow_docker:latest {os.path.join(root_path, 'airflow')}")
    # Run docker-compose
    print('\n- Running docker compose...'.upper())
    run_command_blocking(f"docker compose -f {os.path.join(root_path, 'airflow/docker-compose.yml')} up -d --build")