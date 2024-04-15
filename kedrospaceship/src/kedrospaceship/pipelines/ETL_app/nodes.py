"""
This is a boilerplate pipeline 'ETL'
generated using Kedro 0.19.2
"""

from typing import Dict, Tuple
import pandas as pd


# Import an instance of MLp which is shared accross the project
from kedrospaceship.mlp_instance import shared_MLp_instance as mlp

def csv_to_parquet(data: pd.DataFrame):
    return data

def get_X_y_data(data: pd.DataFrame, params: Dict) -> Tuple:
    y = data[params['target']]
    X = data.drop(params['target'], axis=1)
    return X, y


