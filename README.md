# MLOpsPipelineOrchestrator

MLp integrate well with kedro for building best-practices complient pipelines.

- Use kedro with MLp to build best-practice compliant data and training pipelines.
- Run the mlflow server to track/access all information about the training + artefacts.
- Use docker to containerize our kedro/MLp project as well as our Airflow scheduler app.
- Use Airflow to schedule the training of the model (to keep the model up to date with potential new data)
- Use kedro_mlflow to serve your model as a pipeline encompassing both data preprocessing and predictions steps.

