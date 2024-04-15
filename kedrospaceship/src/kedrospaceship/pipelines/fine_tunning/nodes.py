"""
This is a boilerplate pipeline 'fine_tunning'
generated using Kedro 0.19.2
"""


import os
from typing import Tuple, Dict, List
import pandas as pd
from kedrospaceship.py_funcs import get_attr_from_module_path


def data_pipelines_and_model_hyperparameter_fine_tunning(X: pd.DataFrame, y: pd.Series, params: Dict, params_model: Dict) -> Tuple:
    # Import an instance of MLp which is shared accross the project
    from kedrospaceship.mlp_instance import shared_MLp_instance as mlp
    
    method_name = params['method']
    
    experiments_file_path = os.path.join(params['directory'], ''.join([method_name, params['file_name_suffix']]))
    hyperparam_experiments = get_attr_from_module_path(method_name, experiments_file_path, params['hyperparams_variable'])
    
    
    kf = None
    if params['predefined_kf']: kf = get_attr_from_module_path('kf', params['kf_path'], params['kf_variable'])
    
    

    if method_name.lower() == 'optuna':
        best_params, best_cv_score, best_score_std = mlp.optuna_tunning(
                                                            hyperparam_experiments, params['optuna_specific_params']['n_trials'], params['scoring'],
                                                            direction=params['optuna_specific_params']['direction'], custom_objective=params['optuna_specific_params']['custom_objective'],
                                                            X=X, y=y,
                                                            kf=kf, n_splits=params['n_splits'], cv_n_jobs=params['cv_n_jobs'], verbose=params['verbose']
                                                        )  

    elif method_name.lower() == 'gridsearch':
        best_params, best_cv_score, best_score_std = mlp.grid_search_tuning(
                                                            hyperparam_experiments, params['scoring'],
                                                            X=X, y=y,
                                                            kf=kf, n_splits=params['n_splits'], cv_n_jobs=params['cv_n_jobs'], verbose=params['verbose']
                                                        ) 
    
    return best_params
    
    
    
    
'''    
    HERE ACCESS mlp_params\FINE_TUNNING dir AND create new file NAMED ACCORDING TO data_pipeline names + name model AND SAVE the parameters separately in a dict (WITH MLP's make_hyperparameters_dict_with_separated_objects method)
    
    # Access the hyperparameters associated to the used model via the defined kedro parameters
    model_name = params['model']['model_name']
    hyper_params_name = 'hyperparameters_best'
    hyperparams_file_path = os.path.join(params['directory'], 
                                         params['hyperparameters']['sub_directory'],  
                                         ''.join([model_name, '_', hyper_params_name, params['file_name_suffix']]))
    hyperparameters = get_attr_from_module_path(hyper_params_name, hyperparams_file_path, params['hyperparameters']['hyperparameters_variable'])
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    get_attr_from_module_path('best_hyperparams', )'''
    
    
    
    

                                 
                                 