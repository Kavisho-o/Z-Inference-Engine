import numpy as np

from ml_engine.training.data_utils import load_train_val_data
from ml_engine.explainability.shap_explainer import RiskSHAPExplainer
from ml_engine.config.feature_config import FEATURE_COLUMNS


DATASET_PATH = "data_pipeline/datasets/final/final_dataset_20260130_103342.csv"
RANDOM_STATE = 42


def run_single_shap_explanation():


    # load deterministic train/val split

    X_train, X_val, y_train, y_val = load_train_val_data(

        csv_path=DATASET_PATH,
        random_state=RANDOM_STATE

    )


    # initialize SHAP explainer with training background only

    explainer = RiskSHAPExplainer(background_data=X_train)


    # take a single validation sample

    sample_index = 0
    X_sample = X_val[sample_index].reshape(1, -1)


    # compute SHAP values

    shap_values = explainer.explain(X_sample)



    print("\n~~~~~~~~~~~~~~~~~~~~~~SHAP Explanation (Single Segment)~~~~~~~~~~~~~~~~~~~~~~")


    print("Feature contributions:\n")

    for name, value in zip(FEATURE_COLUMNS, shap_values[0]):

        print(f"{name:<25} : {value:+.4f}")




if __name__ == "__main__":
    
    run_single_shap_explanation()
