'''

using RF because it is:

    1.Robust to noise
    2.Handles ordinal encodings correctly
    3.Strong bias~variance balance
    4.Interpretable feature importance
    5.Excellent baseline for synthetic teacher labels


this script:
- loads and validates training data
- trains a RandomForestRegressor
- evaluates performance on validation set
- persists model and metadata


this model serves as a sanity anchor before moving to XGBoost.


'''


import json
import joblib
import numpy as np
from datetime import datetime,timezone
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

from ml_engine.training.data_utils import load_train_val_data
from ml_engine.config.feature_config import FEATURE_COLUMNS, TARGET_COLUMN




DATASET_PATH = "data_pipeline/datasets/final/final_dataset_20260130_103342.csv"

MODEL_OUTPUT_PATH = "ml_engine/models/rf_model.pkl"
METADATA_OUTPUT_PATH = "ml_engine/models/model_metadata_rf.json"

RANDOM_STATE = 42




RF_PARAMS = {

    "n_estimators": 200,
    "max_depth": None,
    "min_samples_split": 5,
    "min_samples_leaf": 2,
    "n_jobs": -1,
    "random_state": RANDOM_STATE

}





# this is the training pipeline

def train_random_forest():


    print("~~~~~~~~~~~~~~~~~~RandomForest Training Started~~~~~~~~~~~~~~~~~~")



    # load data
    X_train, X_val, y_train, y_val = load_train_val_data(
        csv_path=DATASET_PATH,
        random_state=RANDOM_STATE
    )



    # train
    model = RandomForestRegressor(**RF_PARAMS)
    model.fit(X_train, y_train)



    # predict
    y_pred = model.predict(X_val)



    # metrics
    mse = mean_squared_error(y_val, y_pred) 
    rmse = np.sqrt(mse)   
    mae = mean_absolute_error(y_val, y_pred)
    r2 = r2_score(y_val, y_pred)




    print("~~~~~~~~~~~~~~~~~~Validation Metrics~~~~~~~~~~~~~~~~~~")

    print(f"RMSE: {rmse:.4f}")
    print(f"MAE : {mae:.4f}")
    print(f"R²  : {r2:.4f}")



    # persist model
    joblib.dump(model, MODEL_OUTPUT_PATH)
    print(f"Model saved to {MODEL_OUTPUT_PATH}")



    # persist metadata
    metadata = {
        "model_type": "RandomForestRegressor",
        "target": TARGET_COLUMN,
        "num_features": len(FEATURE_COLUMNS),
        "features": FEATURE_COLUMNS,
        "hyperparameters": RF_PARAMS,
        "metrics": {
            "rmse": rmse,
            "mae": mae,
            "r2": r2
        },
        "dataset_path": DATASET_PATH,
        "random_state": RANDOM_STATE,
        "created_at": datetime.now(timezone.utc).isoformat()
    }



    with open(METADATA_OUTPUT_PATH, "w") as f:

        json.dump(metadata, f, indent=4)



    print(f"Metadata saved to {METADATA_OUTPUT_PATH}")


if __name__ == "__main__":

    train_random_forest()





'''

Our baseline RF achieves very high R² because it is trained on synthetic, 
rule-generated labels using engineered abstractions derived from the same domain logic. 
We explicitly validate this behavior and treat the model as a consistency learner, 
not a real-world performance estimate.

'''