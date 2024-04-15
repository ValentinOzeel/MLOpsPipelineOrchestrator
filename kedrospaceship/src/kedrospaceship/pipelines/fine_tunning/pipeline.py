"""
This is a boilerplate pipeline 'fine_tunning'
generated using Kedro 0.19.2
"""

from kedro.pipeline import Pipeline, pipeline, node


from .nodes import data_pipelines_and_model_hyperparameter_fine_tunning 

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=data_pipelines_and_model_hyperparameter_fine_tunning,
                inputs=["X", "y", "params:FINE_TUNNING", "params:MODEL"],
                outputs="best_hyperparameters",
                name="data_pipelines_and_model_hyperparameter_fine_tunning_node",
            ),
                    
     
    ]
        )
