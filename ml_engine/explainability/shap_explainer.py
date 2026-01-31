import joblib
import shap
import numpy as np

from ml_engine.config.feature_config import FEATURE_COLUMNS


MODEL_PATH = "ml_engine/models/rf_model.pkl"


class RiskSHAPExplainer:

    
    # Wrapper around SHAP TreeExplainer for ZEPHYR risk model.


    def __init__(self, background_data: np.ndarray):

        
        # background_data: numpy array of training features


        self.model = joblib.load(MODEL_PATH)

        self.explainer = shap.TreeExplainer(

            self.model,
            data=background_data,
            feature_names=FEATURE_COLUMNS

        )



    def explain(self, X: np.ndarray):


        """

        compute SHAP values for input samples.

        Returns: shap_values: np.ndarray (n_samples, n_features)


        """

        
        shap_values = self.explainer.shap_values(X)
        return shap_values
