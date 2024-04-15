# Import MLp
from MLp.src.MLp_builder import MLpBuilder

'''
Import the function {_get_conf_data} from the file {src/{your_kedro_project}/kedro_funcs.py}
    Run {_get_conf_data} to access kedro parameters (located in conf)
    Access the dictionary parameter {MLP_CONFIG}
'''
from .kedro_funcs import _get_conf_data
parameters = _get_conf_data(load='parameters')
kedro_params_MLP_CONFIG = parameters['MLP_CONFIG']


class SingletonSharedMLp(MLpBuilder):
    '''
    SingletonSharedMLp inherits from MLpBuilder class and is intended to act as a shared data structure for MLp accross kedro's pipelines. 
    The class uses a design pattern called the Singleton, which ensures that only one instance of the class is created during the lifetime of the program.
    '''
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SingletonSharedMLp, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
shared_MLp_instance = SingletonSharedMLp()
# Import the function set_mlp_config that update MLp's configuration file 
from MLp.conf.config_functions import set_config
# Modify MLp's config file with MLP_CONFIGS
set_config('MLP_CONFIG', kedro_params_MLP_CONFIG)








    
    
    