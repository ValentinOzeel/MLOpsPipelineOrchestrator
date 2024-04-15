
#####################################################################
#                      SAMPLING STEPS 
#####################################################################


from MLp.src.preprocessing.MLp_preprocessing_transformers import LogScalerTransformer
from MLp.src.preprocessing.MLp_sampling_transformers import IQROutliersTransformer, DropNaTransformer


pipeline_steps = [
    (
        '*log_scaler',
        LogScalerTransformer,
        {'columns': ['VRDeck', 'Spa', 'FoodCourt', 'ShoppingMall', 'RoomService']}
    ),
    (
        '*iqr_outliers',
        IQROutliersTransformer,
        {'columns': ['VRDeck', 'Spa', 'FoodCourt', 'ShoppingMall', 'RoomService'],
         'IQR_multiplier': 1.5},
        
    ),
#    ('*drop_na', DropNaTransformer, {'columns':'all'})

]
