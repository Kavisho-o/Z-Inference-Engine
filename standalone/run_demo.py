from ml_engine.training.data_utils import load_train_val_data
from ml_engine.explainability.shap_explainer import RiskSHAPExplainer
from ml_engine.explainability.explanation_formatter import ExplanationFormatter
from ml_engine.config.feature_config import FEATURE_COLUMNS
from ml_engine.models.rf_model import load_model



'''

FOR DEMO PURPOSES ONLY
NOT A PART OF ZEPHYR
THIS IS A DEMO FOR THE STANDALONE ML MODEL

IF YOU ARE TRYING THIS MODEL OUT, MY HEARTIEST GREETINGS TO YOU.
I HAVE PUT A LOT OF EFFORT INTO SYNTHESIZING THE DATA, SO DO GO THROUGH THE DEV LOGS.
ENJOY <3.


'''



DATASET_PATH = "data_pipeline/datasets/final/final_dataset_20260130_103342.csv"
RANDOM_STATE = 42


def risk_class_from_score(score: float) -> str:

    if score < 30:

        return "Safe"
    

    if score < 60:

        return "Moderate"
    

    return "Dangerous"




def run_demo():

    # load data 

    X_train, X_val, y_train, y_val = load_train_val_data(
        csv_path=DATASET_PATH,
        random_state=RANDOM_STATE
    )


    # load model

    model = load_model()


    # initialize SHAP explainer with training background

    shap_explainer = RiskSHAPExplainer(background_data=X_train)
    formatter = ExplanationFormatter(FEATURE_COLUMNS)


    # pick one sample

    sample_index = 0
    X_sample = X_val[sample_index].reshape(1, -1)


    # predict

    risk_score = float(model.predict(X_sample)[0])
    risk_class = risk_class_from_score(risk_score)


    # explaination 

    shap_values = shap_explainer.explain(X_sample)[0]
    explanation = formatter.format(shap_values)



    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~DEMO RESULTS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
    
    print(f"Risk Score : {risk_score:.2f}")
    print(f"Risk Class : {risk_class}\n")


    print("Risk Increasing Factors:")

    for item in explanation["risk_increasing_factors"]:

        print(f"  ↑ {item}")
        

    print("\nRisk Mitigating Factors:")

    for item in explanation["risk_mitigating_factors"]:

        print(f"  ↓ {item}")


    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~END OF RESULTS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")



if __name__ == "__main__":

    run_demo()
