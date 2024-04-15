hyperparam_experiments = {
    ###### Preprocessor transformer's parameter tuning
  #  'preprocessing__kmeans_clustering_transformer-1__n_clusters': [10, 25],
    
    ###### Model's hyperparameter tuning
    'model__learning_rate': [0.2],
#    'model__max_depth': [3],
    'model__n_estimators': [50, 200],
#   'model__reg_alpha': [0.001, 0.001, 0.1, 0.5],
#   'model__reg_lambda': [0.001, 0.001, 0.1, 1, 3],
}