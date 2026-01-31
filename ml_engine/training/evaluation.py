import json
import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error

from ml_engine.config.feature_config import FEATURE_COLUMNS
from ml_engine.training.data_utils import load_train_val_data



MODEL_PATH = "ml_engine/models/rf_model.pkl"



def analyze_feature_importance(top_k=10):


    model = joblib.load(MODEL_PATH)


    importances = model.feature_importances_
    pairs = list(zip(FEATURE_COLUMNS, importances))


    pairs.sort(key=lambda x: x[1], reverse=True)



    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~Feature Importance (RandomForest)~~~~~~~~~~~~~~~~~~~~~~~~~~~~")


    for name, score in pairs[:top_k]:

        print(f"{name:<25} : {score:.4f}")


    return pairs



# if __name__ == "__main__":
    
#     analyze_feature_importance()



def bucket_error_analysis(y_true, y_pred):


    buckets = {

        "0-20": (0, 20),
        "20-40": (20, 40),
        "40-60": (40, 60),
        "60-80": (60, 80),
        "80-100": (80, 100),

    }


    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~Bucket-wise MAE~~~~~~~~~~~~~~~~~~~~~~~~~")


    for name, (low, high) in buckets.items():

        idx = (y_true >= low) & (y_true < high)

        if idx.sum() == 0:
            continue

        mae = mean_absolute_error(y_true[idx], y_pred[idx])

        print(f"{name:<8} : MAE = {mae:.3f}")





# if __name__ == "__main__":

#     # load trained model

#     model = joblib.load(MODEL_PATH)


#     # load deterministic train/val split

#     X_train, X_val, y_train, y_val = load_train_val_data(

#         csv_path="data_pipeline/datasets/final/final_dataset_20260130_103342.csv",
#         random_state=42

#     )


#     # predict on validation set

#     y_pred = model.predict(X_val)


#     # bucket-wise error analysis

#     bucket_error_analysis(y_val, y_pred)





def noise_sensitivity_test(model, X_val, y_val, noise_std=0.05):


    rng = np.random.default_rng(42)
    X_noisy = X_val + rng.normal(0, noise_std, X_val.shape)


    y_pred_noisy = model.predict(X_noisy)


    mae = mean_absolute_error(y_val, y_pred_noisy)


    print(f"\nNoise Sensitivity Test (sigma={noise_std})")
    print(f"MAE after noise: {mae:.4f}")




# if __name__ == "__main__":


#     # load trained model

#     model = joblib.load(MODEL_PATH)


#     # load deterministic validation split

#     X_train, X_val, y_train, y_val = load_train_val_data(

#         csv_path="data_pipeline/datasets/final/final_dataset_20260130_103342.csv",
#         random_state=42

#     )


#     # baseline prediction (clean validation data)

#     y_pred_clean = model.predict(X_val)
#     baseline_mae = mean_absolute_error(y_val, y_pred_clean)


#     print("\n~~~~~~~~~~~~~~~~~~Baseline Validation MAE~~~~~~~~~~~~~~~~~~")
    
#     print(f"Baseline MAE: {baseline_mae:.4f}")



#     # noise sensitivity test (controlled Gaussian noise)

#     rng = np.random.default_rng(42)
#     noise_std = 0.05

#     X_noisy = X_val + rng.normal(0, noise_std, X_val.shape)

#     y_pred_noisy = model.predict(X_noisy)
#     noisy_mae = mean_absolute_error(y_val, y_pred_noisy)


#     print("\n~~~~~~~~~~~~~~~~~~Noise Sensitivity Test~~~~~~~~~~~~~~~~~~")

#     print(f"Noise std dev : {noise_std}")
#     print(f"MAE w/ noise : {noisy_mae:.4f}")
#     print(f"MAE delta    : {noisy_mae - baseline_mae:.4f}")




def stress_test_slices(X_val, y_val):

    """

    Perform cross-distribution stress testing on validation data.
    Evaluates MAE under meaningful conditional slices.


    """


    # reconstruct dataframe from validation features

    df = pd.DataFrame(X_val, columns=FEATURE_COLUMNS)
    df["risk_score"] = y_val


    slices = {

        "Monsoon == 1": df["monsoon_flag"] == 1,
        "Monsoon == 0": df["monsoon_flag"] == 0,

        "Night == 1": df["night_flag"] == 1,
        "Night == 0": df["night_flag"] == 0,

        "High Traffic (>=60)": df["traffic_risk_index"] >= 60,
        "Low Traffic (<60)": df["traffic_risk_index"] < 60,

        "Mountain Terrain": df["terrain_enc"] == 3,
        "Non-Mountain Terrain": df["terrain_enc"] < 3,

    }

    model = joblib.load(MODEL_PATH)

    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~Stress Test Results~~~~~~~~~~~~~~~~~~~~~~~~~")

    for name, mask in slices.items():

        subset = df[mask]

        if len(subset) == 0:

            continue


        X_slice = subset[FEATURE_COLUMNS].values
        y_slice = subset["risk_score"].values


        y_pred_slice = model.predict(X_slice)
        mae = mean_absolute_error(y_slice, y_pred_slice)


        print(f"{name:<25} | Samples: {len(subset):<5} | MAE: {mae:.4f}")




if __name__ == "__main__":

    # load trained model

    model = joblib.load(MODEL_PATH)


    # load deterministic validation split

    X_train, X_val, y_train, y_val = load_train_val_data(

        csv_path="data_pipeline/datasets/final/final_dataset_20260130_103342.csv",
        random_state=42

    )


    # baseline MAE (for reference)

    y_pred = model.predict(X_val)
    baseline_mae = mean_absolute_error(y_val, y_pred)
    

    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~Baseline Validation~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(f"Baseline MAE: {baseline_mae:.4f}")


    # run stress tests

    stress_test_slices(X_val, y_val)


