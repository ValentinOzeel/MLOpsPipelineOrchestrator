"""
This is a boilerplate pipeline 'ETL'
generated using Kedro 0.19.2
"""


from kedro.pipeline import Pipeline, node, pipeline
from .nodes import csv_to_parquet, get_X_y_data

from kedrospaceship.kedro_funcs import _get_conf_data

def create_pipeline(**kwargs) -> Pipeline:
    
    parameters = _get_conf_data(load='parameters')
    etl_params = parameters['ETL']
    training_dataset_to_load = ''.join([etl_params['file_name_wo_extension'], etl_params['dataset_suffix_mark']])
    
    return pipeline(
        [
        
            node(
                func=csv_to_parquet,
                inputs=training_dataset_to_load,
                outputs="02_reformatted.training_dataset@parquet",
                name="csv_to_parquet_node",
                tags=["etl"]
            ),
        
            node(
                func=get_X_y_data,
                inputs=["02_reformatted.training_dataset@parquet", "params:ETL"],
                outputs=["02_reformatted.X@parquet", "02_reformatted.y@csv"],
                name="get_X_y_data_node",
                tags=["etl"]
            )

        ]
    )
    
