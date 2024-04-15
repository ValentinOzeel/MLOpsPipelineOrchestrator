"""
This is a boilerplate pipeline 'data_split'
generated using Kedro 0.19.2
"""
import pandas as pd
from typing import Dict, Tuple
from kedrospaceship.py_funcs import set_unnamed0_col_as_index
# Import an instance of MLp which is shared accross the project
from kedrospaceship.mlp_instance import shared_MLp_instance as mlp

def initialize_data(X:pd.DataFrame, y:pd.Series, params):
    y=set_unnamed0_col_as_index(y)
    y=y[params['target']]
    return mlp.initialize_data(X=X, y=y,
                               data_copy=params['data_copy'],
                               try_y_as_num=params['try_y_as_num'],
                               print_data_info=params['print_data_info']
                               )
    
def split_data(X: pd.DataFrame, y, parameters: Dict) -> Tuple:
    y=set_unnamed0_col_as_index(y)
    return mlp._split_data(
        X, y, parameters["test_size"],
        shuffle=parameters["shuffle"], random_state=parameters["random_state"], pre_split=parameters["pre_split"], 
    )  
    
    
    
    
