'''

this file is supposed to be the entry point for the model
the model can not access the csv files directly now

objectives:
    1. Load a specified final_dataset_*.csv
    2. Validate schema against feature_config.py
    3. Split data deterministically
    4. Return clean numpy arrays for models
    5. Enforce no leakage / no NaNs
    6. Perform deterministic train/validation split

    
'''





import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

from ml_engine.config.feature_config import (
    FEATURE_COLUMNS,
    TARGET_COLUMN,
    FORBIDDEN_COLUMNS
)


DEFAULT_RANDOM_STATE = 42
DEFAULT_TEST_SIZE = 0.2


def load_and_validate_dataset(csv_path: str) -> pd.DataFrame:


    """

    Load final dataset CSV and validate schema strictly.

    Parameters->
    csv_path : str
        Path to final_dataset_*.csv

    Returns->
    pd.DataFrame
        Validated dataframe (unchanged, no mutation)


    """

    if not os.path.exists(csv_path):

        raise FileNotFoundError(f"Dataset file not found: {csv_path}")
    

    df = pd.read_csv(csv_path)


    if df.empty:

        raise ValueError("Loaded dataset is empty.")
    


    required_columns = set(FEATURE_COLUMNS + [TARGET_COLUMN])                           # required columns
    missing_columns = required_columns - set(df.columns)

    if missing_columns:

        raise ValueError(
            f"Dataset is missing required columns: {sorted(missing_columns)}"
        )
    


    
    leaking_columns = set(FORBIDDEN_COLUMNS).intersection(FEATURE_COLUMNS)                   # forbidden columns check

    if leaking_columns:
        
        raise ValueError(
            f"Forbidden columns included in FEATURE_COLUMNS: {sorted(leaking_columns)}"
        )
    

    nan_feature_cols = df[FEATURE_COLUMNS].isnull().any()                               # NaN check
    nan_feature_cols = nan_feature_cols[nan_feature_cols].index.tolist()


    if nan_feature_cols:

        raise ValueError(
            f"NaN values detected in feature columns: {nan_feature_cols}"
        )
    

    if df[TARGET_COLUMN].isnull().any():

        raise ValueError("NaN values detected in target column.")
    


    # eliminated any chance of abnormality in the data, so now we can log our success

    print("\n~~~~~~~~~~~~~~~~~~Dataset loaded successfully~~~~~~~~~~~~~~~~~~\n")

    print(f"  Rows: {len(df)}")
    print(f"  Features: {len(FEATURE_COLUMNS)}")
    print(f"  Target: {TARGET_COLUMN}")


    return df


def prepare_train_val_split(
    df: pd.DataFrame,
    test_size: float = DEFAULT_TEST_SIZE,
    random_state: int = DEFAULT_RANDOM_STATE
):
    

    """

    
    prepare deterministic train/validation split.

    parameters

    df : pd.DataFrame (validated dataset)
    test_size : float (fraction of data for validation)
    random_state : int (seed for reproducibility)

    returns

    X_train, X_val, y_train, y_val : np.ndarray

    

    """


    X = df[FEATURE_COLUMNS].values
    y = df[TARGET_COLUMN].values


    X_train, X_val, y_train, y_val = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        shuffle=True
    )


    print("\n~~~~~~~~~~~~~~~~~~Train/validation split created~~~~~~~~~~~~~~~~~~\n")

    print(f"  Train size: {len(X_train)}")
    print(f"  Validation size: {len(X_val)}")
    print(f"  Random state: {random_state}")


    return X_train, X_val, y_train, y_val


def load_train_val_data(
    csv_path: str,
    test_size: float = DEFAULT_TEST_SIZE,
    random_state: int = DEFAULT_RANDOM_STATE
):
    

    """

    high-level convenience wrapper used by training scripts
    this is the ONLY function training scripts should call

    returns
    X_train, X_val, y_train, y_val : np.ndarray


    """


    df = load_and_validate_dataset(csv_path)


    return prepare_train_val_split(
        df,
        test_size=test_size,
        random_state=random_state
    )





# i mean i couldve done it normally through the csv file as well but i did this because
# now all training data passes through a strict validation layer that enforces schema, prevents leakage, and guarantees reproducibility