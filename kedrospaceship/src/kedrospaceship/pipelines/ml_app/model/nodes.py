"""
This is a boilerplate pipeline 'model'
generated using Kedro 0.19.2
"""

import os 
from typing import Tuple, Dict
import pandas as pd
from kedrospaceship.py_funcs import get_attr_from_module_path
# Import an instance of MLp
from kedrospaceship.mlp_instance import shared_MLp_instance as mlp
from kedrospaceship.py_funcs import set_unnamed0_col_as_index
    
def train_model(X_train: pd.DataFrame, y_train: pd.Series, 
                params: Dict):

    y_train = set_unnamed0_col_as_index(y_train)
    
    # Access the model via the defined kedro parameters
    model_name = params['model']['model_name']
    model_file_path = os.path.join(params['directory'], 
                                   ''.join([model_name, params['file_name_suffix']]))
    model_variable = params['model']['model_variable']
    model = get_attr_from_module_path(model_name, model_file_path, model_variable)
    
    # Access the model's hyperparameters via the defined kedro parameters
    hyperparams_name = params['hyperparameters']['hyperparameters_name']
    hyperparams_associated_model_name = ''.join([model_name, '_', hyperparams_name])
    hyperparams_sub_dir = params['hyperparameters']['sub_directory']
    hyperparams_file_path = os.path.join(params['directory'], 
                                         hyperparams_sub_dir,  
                                         ''.join([hyperparams_associated_model_name, params['file_name_suffix']]))
    hyperparams_variable = params['hyperparameters']['hyperparameters_variable']
    hyperparameters = get_attr_from_module_path(hyperparams_associated_model_name, hyperparams_file_path, hyperparams_variable)


    model = model(**hyperparameters)
    mlp.define_model(use_model=model, model_name=params['model'])
    # Fit the model on the training data
    model.fit(X_train, y_train) 
    
    return model


def evaluate_model(X_train: pd.DataFrame, y_train: pd.Series, 
                     X_test: pd.DataFrame, y_test: pd.Series, 
                     model, params: Dict):
    
    y_train = set_unnamed0_col_as_index(y_train)
    y_test = set_unnamed0_col_as_index(y_test)
    
    scoring = params['scoring']
    # Make predictions on the test data and get the test score
    predictions = model.predict(X_test)
    test_score_value = mlp.evaluate_model_get_score(scoring, y_test, predictions)
    
    print(f"Performance on train data: {scoring} = {model.score(X_train, y_train)}")
    print(f"Performance on test data: {scoring} = {test_score_value}")
    
    return# model.score(X_train, y_train), test_score_value


def make_inferences(to_predict: pd.DataFrame, 
                   model):
    return model.predict(to_predict)
            
        
        
        
