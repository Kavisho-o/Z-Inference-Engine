import numpy as np

from ml_engine.config.feature_config import FEATURE_DESCRIPTIONS


class ExplanationFormatter:
    
    # converts raw SHAP values into human-readable explanations.


    def __init__(self, feature_names):

        self.feature_names = feature_names


    def format(self, shap_values, top_k=3):

        # shap_values: np.ndarray of shape (n_features,)
        # returns a structured explanation dict.


        pairs = list(zip(self.feature_names, shap_values))
        pairs.sort(key=lambda x: abs(x[1]), reverse=True)


        positive = [(f, v) for f, v in pairs if v > 0][:top_k]
        negative = [(f, v) for f, v in pairs if v < 0][:top_k]


        explanation = {
           
            "risk_increasing_factors": [
                f"Increased risk due to {FEATURE_DESCRIPTIONS[f]}"
                for f, _ in positive
            ],
            "risk_mitigating_factors": [
                f"Reduced risk due to favorable {FEATURE_DESCRIPTIONS[f]}"
                for f, _ in negative
            ]
            
        }

        return explanation
