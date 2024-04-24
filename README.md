# MLOpsPipelineOrchestrator

MLp integrate well with kedro for building best-practices complient pipelines.

- Use kedro with MLp to build best-practice compliant data and training pipelines.
- Run the mlflow server to track/access all information about the training + artefacts.
- Use docker to containerize our kedro/MLp project as well as our Airflow scheduler app.
- Use Airflow to schedule the training of the model (to keep the model up to date with potential new data)
- Use kedro_mlflow to serve your model as a pipeline encompassing both data preprocessing and predictions steps.




How to use:

- Clone the github repo: 
git clone https://github.com/ValentinOzeel/MLOpsPipelineOrchestrator.git

- Modify environment PATHs (project root) in airflow\docker-compose.yml

- Potentially modify the scheduler starting date in config airflow/conf/airflowconfig.yml

- To initialize and run the app:
python initialize.py

Afterwards, executing: ---- docker compose -f "airflow\docker-compose.yml" up -d --build ---- will suffice to launch the app.

Wait a minute after running the container and access airflow UI:
http://localhost:8080

Stop the container:
docker stop airflow-airflow_docker-1

Access Mlflow UI:
cd kedrospaceship
mlflow ui
Go to http://127.0.0.1:5000

For inference serving, modify the run id in kedrospaceship\conf\base\parameters_serving_inference.yml before running:
cd kedrospaceship\src\kedrospaceship
python inference_serving.py

