'''


this is the main course of passage for all the features, we will engineer the features here

finalized features:

| Feature            | Type  | Range         | Why                    |
| ------------------ | ----- | ------------- | ---------------------- |
| rain_risk          | float | 0 to 1        | Accident + delay risk  |
| wind_risk          | float | 0 to 1        | Vehicle stability      |
| visibility_risk    | float | 0 to 1        | Human perception       |
| slope_risk         | float | 0 to 1        | Brake + control        |
| traffic_risk_index | int   | 0 to 100      | Operational congestion |
| night_flag         | int   | 0/1           | Visibility + fatigue   |
| monsoon_flag       | int   | 0/1           | Systemic seasonal risk |
| road_type_enc      | int   | small ordinal | Infrastructure quality |
| terrain_enc        | int   | small ordinal | Structural difficulty  |


'''




from .risk_transformers import (

    rain_to_risk,
    wind_to_risk,
    visibility_to_risk,
    slope_to_risk

)


from .encoders import encode_road_type, encode_terrain




def engineer_features(segment: dict) -> dict:


    # convert enriched segment data into ML-ready features
    # this must remain deterministic and inference-safe


    rain_risk = rain_to_risk(segment["rain_intensity"])

    wind_risk = wind_to_risk(segment["wind_speed"])

    visibility_risk = visibility_to_risk(segment["visibility"])

    slope_risk = slope_to_risk(segment["slope"])

    night_flag = 1 if (segment["hour"] < 6 or segment["hour"] > 18) else 0

    monsoon_flag = 1 if 6 <= segment["month"] <= 9 else 0

    road_type_enc = encode_road_type(segment["road_type"])

    terrain_enc = encode_terrain(segment["terrain_type"])


    return {

        "rain_risk": rain_risk,
        "wind_risk": wind_risk,
        "visibility_risk": visibility_risk,
        "slope_risk": slope_risk,
        "traffic_risk_index": segment["traffic_risk_index"],
        "night_flag": night_flag,
        "monsoon_flag": monsoon_flag,
        "road_type_enc": road_type_enc,
        "terrain_enc": terrain_enc,
        
    }