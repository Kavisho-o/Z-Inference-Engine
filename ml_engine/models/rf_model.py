import joblib
import os


MODEL_PATH = "ml_engine/models/rf_model.pkl"



def load_model():
    
    
    # Load the trained RandomForest risk model.
    # Returns: sklearn RandomForestRegressor


    if not os.path.exists(MODEL_PATH):

        raise FileNotFoundError(
            f"Trained model not found at {MODEL_PATH}. "
            "Ensure the model has been trained and saved."
        )
    

    return joblib.load(MODEL_PATH)
