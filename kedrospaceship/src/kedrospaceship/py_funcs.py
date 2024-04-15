import importlib
from typing import List

def get_attr_from_module_path(name, path, attr):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    # Use getattr to retrieve the variable dynamically
    if isinstance(attr, str):
        return getattr(module, attr, None)
    
    elif isinstance(attr, List):
        return [getattr(module, var, None) for var in attr]
    
    
def set_unnamed0_col_as_index(pd_objet):
    '''
    y_train and y_test are saved as pandas.CSVDataset, however the index is added as a column 'Unnamed: 0'
    The function set the columns 'Unnamed: 0' as index and drop the column.
    '''
    if 'Unnamed: 0' in pd_objet.columns.tolist():
        index=pd_objet['Unnamed: 0']
        pd_objet = pd_objet.drop(columns=['Unnamed: 0'])
        pd_objet.set_index(index, inplace=True)
        pd_objet.index.name = None
    return pd_objet

