import pandas as pd
import os
from kedro_funcs import _get_conf_data
parameters = _get_conf_data(load='parameters')
serving_inference_params = parameters['SERVING_INFERENCE']

# Assuming you are currently in your_kedro_project_dir/src/your_kedro_project/inference_serving.py
PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
PROJECT_NAME = serving_inference_params['PROJECT_NAME']
MLFLOW_RUN_ID = serving_inference_params['MLFLOW_RUN_ID']
TO_PREDICT_PATH = serving_inference_params['TO_PREDICT_PATH']

from kedro.framework.startup import bootstrap_project
from kedro.framework.session import KedroSession
from mlflow.pyfunc import load_model

def run_best_model_inference():
  
  bootstrap_project(PROJECT_PATH)
  session = KedroSession.create(
    project_path=PROJECT_PATH,
  )
  local_context = session.load_context() # setup mlflow config
  
  # Load mlflow model (inference pipeline)
  model = load_model(f"runs:/{MLFLOW_RUN_ID}/{PROJECT_NAME}")

  to_predict = pd.read_csv(TO_PREDICT_PATH)
  predictions = model.predict(to_predict)
  
  return (predictions)

predicts = run_best_model_inference()
print(predicts)