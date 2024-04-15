"""
This is a boilerplate pipeline 'data_pipelines'
generated using Kedro 0.19.2
"""

import os
from typing import Tuple, Dict, List
import pandas as pd
from kedrospaceship.py_funcs import get_attr_from_module_path
# Import an instance of MLp as well as kedro's MLP_CONFIG parameter (located in conf/base/parameters.yml)
from kedrospaceship.mlp_instance import shared_MLp_instance as mlp


def create_data_pipelines(params: Dict) -> Tuple:
    data_pipelines = []
    for pipeline_name in params['pipelines']:

        steps_file_path = os.path.join(params['directory'], ''.join([pipeline_name, params['file_name_suffix']]))
        pipeline_steps = get_attr_from_module_path(pipeline_name, steps_file_path, params['steps_variable'])
        
    
        ## Define the pipeline
        pipeline = mlp.create_data_pipeline(
                        name=pipeline_name,
                        steps=pipeline_steps
                    )
    
        data_pipelines.append((pipeline_name, pipeline))
        
    return data_pipelines


def apply_data_pipelines_fit_transform(X:pd.DataFrame, list_pipelines:List) -> Tuple:
    for pipeline_name, pipeline in list_pipelines:
        X = mlp.apply_data_pipeline((pipeline_name, pipeline), X_fit_tr=X)
    return X, list_pipelines


def apply_data_pipelines_transform(X:pd.DataFrame, list_fitted_pipelines:List) -> Tuple:
    for fitted_pipeline_name, fitted_pipeline in list_fitted_pipelines:
        X = mlp.apply_data_pipeline((fitted_pipeline_name, fitted_pipeline), X_transform=X)
    return X

def drop_sampled_index_in_y(X:pd.DataFrame, y:pd.Series):
    y = mlp.remove_dropped_index_in_y(X, y)
    return y