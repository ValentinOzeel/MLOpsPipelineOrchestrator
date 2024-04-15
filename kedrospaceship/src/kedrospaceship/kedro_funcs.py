import os 
from kedro.config import OmegaConfigLoader
from kedro.io import DataCatalog

def _get_conf_data(conf_path=None, load="catalog"):
    if conf_path is None:
        # Assuming you are currently in your_kedro_project_dir/src/your_kedro_project/kedro_funcs.py
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        conf_path = os.path.join(project_root, 'conf')

    conf_path = conf_path.encode('unicode-escape').decode()
    conf_loader = OmegaConfigLoader(conf_source=conf_path)

    if load.lower() == 'catalog':
        return DataCatalog.from_config(conf_loader[load])
    elif load.lower() == 'parameters':
        return conf_loader.get(load)
    else:
        raise ValueError('load value should be catalog or parameters.')