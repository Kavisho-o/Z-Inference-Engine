'''

this file is purely declarative and not meant for execution purposes
nevertheless, it is very important as it answers the questions:

from this point onward:
-> nothing is allowed to invent features
-> nothing is allowed to reorder columns
-> nothing is allowed to “just drop” something silently

 
this file will contain 4 things:
    1. input feature columns (order-wise)
    2. target column
    3. forbidden columns (non-features)
    4. descriptions (in english) : for SHAP predicitions later


'''




FEATURE_COLUMNS = [

    "rain_risk",            # derived from rain_intensity
    "wind_risk",            # derived from wind_speed
    "visibility_risk",      # derived from visibility
    "slope_risk",           # derived from terrain slope
    "traffic_risk_index",   # operational congestion + delay proxy
    "night_flag",           # binary contextual risk
    "monsoon_flag",         # seasonal risk amplifier
    "road_type_enc",        # ordinal road risk encoding
    "terrain_enc"           # ordinal terrain risk encoding

]




TARGET_COLUMN = "risk_score"



FORBIDDEN_COLUMNS = [

    "risk_class",               # derived label
    "route_id",
    "segment_id",
    "start_lat",
    "start_lon",
    "end_lat",
    "end_lon",
    "segment_length_km",
    "total_route_length_km",
    "month",
    "hour",
    "rain_intensity",
    "wind_speed",
    "temperature",
    "visibility",
    "elevation",
    "slope",
    "road_type",
    "terrain_type"

]




FEATURE_DESCRIPTIONS = {          # just for reference and will be changed later

    "rain_risk": "rainfall intensity conditions",
    "wind_risk": "wind speed conditions",
    "visibility_risk": "visibility conditions (fog, rain, night)",
    "slope_risk": "road slope and steepness",
    "traffic_risk_index": "traffic congestion conditions",
    "night_flag": "time-of-day driving conditions",
    "monsoon_flag": "seasonal monsoon-related conditions",
    "road_type_enc": "road infrastructure type",
    "terrain_enc": "surrounding terrain characteristics"

}


