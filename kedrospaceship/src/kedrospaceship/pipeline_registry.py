"""Project pipelines."""
from typing import Dict

from kedro.pipeline import Pipeline

from kedro_mlflow.pipeline import pipeline_ml_factory

from .pipelines.ETL_app.pipeline import create_pipeline as create_etl_pipeline
from .pipelines.ml_app.pipeline import create_pipeline as create_ml_pipeline



def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.
    
    Bind inference pipeline to the training pipeline with pipeline_ml_factory.
    Here we include the ETL pipeline in the training framework for demo purpose.

    Returns:
        A mapping from pipeline names to ``Pipeline`` objects.
    """
    
    etl_pipeline, ml_pipeline = create_etl_pipeline(), create_ml_pipeline()
    inference_ml_pipeline = ml_pipeline.only_nodes_with_tags("inference")
    training_ml_pipeline = ml_pipeline.only_nodes_with_tags("training")
    
    # Bind inference pipeline to the training pipeline (inference as artefact every time training is run)
    # Enable to serve your model as an inference pipeline (with data preprocessing)
    training_ml_pipeline = pipeline_ml_factory(
                  # ETL included in the training framework
        training=etl_pipeline + training_ml_pipeline,
        inference=inference_ml_pipeline,
        input_name="to_predict",
        log_model_kwargs=dict(
            artifact_path="kedrospaceship",
            signature="auto",
        )
    )
    
    return {
        "etl": etl_pipeline,
        "training": training_ml_pipeline,
        "inference": inference_ml_pipeline,

        "__default__": training_ml_pipeline
    }





