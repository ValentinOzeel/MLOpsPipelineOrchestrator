"""
This is a boilerplate pipeline 'data_pipelines'
generated using Kedro 0.19.2
"""

from kedro.pipeline import Pipeline, pipeline, node

from .initialize_data.nodes import split_data, initialize_data

from .data_pipelines.nodes import (
    create_data_pipelines, 
    apply_data_pipelines_fit_transform, 
    apply_data_pipelines_transform,
    drop_sampled_index_in_y
    )

from .model.nodes import (
    train_model, 
    evaluate_model, 
    make_inferences
    )

def create_pipeline(**kwargs) -> Pipeline:
    
    initialize_data_pipeline = pipeline(
        [
            node(
                name="initialize_data_node",
                func=initialize_data,
                inputs=["02_reformatted.X@parquet", "02_reformatted.y@csv", "params:INITIALIZE"],
                outputs=["03_primary.X@parquet", "03_primary.y@csv"],
                tags=["training"]
            ),
            
            
            node(
                name="split_data_node",
                func=split_data,
                inputs=["03_primary.X@parquet", "03_primary.y@csv", "params:DATA_SPLIT"],
                outputs=["X_train", "X_test", 
                        "y_train", "y_test"],
                tags=["training"]
            )
        ]
    )


    
    data_preprocess_pipeline = pipeline(
        [
            node(
                name="create_data_pipelines_node",
                func=create_data_pipelines,
                inputs="params:DATA_PIPELINES",
                outputs="list_data_pipelines",
                tags=["training"]
            ),
                    
            node(
                name="apply_data_pipelines_train_data_node",
                func=apply_data_pipelines_fit_transform,
                inputs=["X_train", 
                        "list_data_pipelines"],
                outputs=["05_model_input.X_train_preprocessed@parquet",
                         "fitted_list_data_pipelines@pkl"],
                tags=["training"]
            ),
            
            
            node(
                name="drop_sampled_index_in_y_train_node",
                func=drop_sampled_index_in_y,
                inputs=["05_model_input.X_train_preprocessed@parquet", "y_train"],
                outputs="05_model_input.y_train_preprocessed@csv",
                tags=["training"]
            ),     
            
            node(
                name="apply_data_pipelines_test_data_node",
                func=apply_data_pipelines_transform,
                inputs=["X_test", 
                        "fitted_list_data_pipelines@pkl"],
                outputs="05_model_input.X_test_preprocessed@parquet",
                tags=["training"]
            ),  
            
            node(
                name="drop_sampled_index_in_y_test_node",
                func=drop_sampled_index_in_y,
                inputs=["05_model_input.X_test_preprocessed@parquet", "y_test"],
                outputs="05_model_input.y_test_preprocessed@csv",
                tags=["training"]
            ), 
            
            node(
                name="apply_data_pipelines_to_predict_data_node",
                func=apply_data_pipelines_transform,
                inputs=["to_predict",
                        "fitted_list_data_pipelines@pkl"],
                outputs="05_model_input.to_predict_preprocessed@parquet",
                tags=["inference"]
            ),          
    ]
        )
    
    
    train_model_pipeline = pipeline(
        [
            node(
                name="train_model_node",
                func=train_model,
                inputs=["05_model_input.X_train_preprocessed@parquet", "05_model_input.y_train_preprocessed@csv",
                        "params:MODEL"],
                outputs="fitted_model@pkl",
                tags=["training"]
            ),
            
            node(
                name="evaluate_model_node",
                func=evaluate_model,
                inputs=["05_model_input.X_train_preprocessed@parquet", "05_model_input.y_train_preprocessed@csv",
                        "05_model_input.X_test_preprocessed@parquet", "05_model_input.y_test_preprocessed@csv",
                        "fitted_model@pkl", "params:MODEL"],
                outputs=None,
                tags=["training", "evaluate"]
            ),
            
            node(
                name="make_inferences_node",
                func=make_inferences,
                inputs=["05_model_input.to_predict_preprocessed@parquet",
                        "fitted_model@pkl"],
                outputs="predictions@csv",
                tags=["inference"]
            ),
            
        ]
    )
    
    return(
       initialize_data_pipeline + data_preprocess_pipeline + train_model_pipeline
    )