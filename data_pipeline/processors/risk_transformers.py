'''


for converting all the labels into workable indexes
these indexes are deterministic, contain no randomness and are usable in inference later

using step wise buckets that can be helpful in SHAP explanations later



'''



def rain_to_risk(rain_mm_hr):


    if rain_mm_hr <= 0:

        return 0.0
    

    if rain_mm_hr < 2:

        return 0.2
    

    if rain_mm_hr < 5:

        return 0.4
    

    if rain_mm_hr < 10:

        return 0.7
    

    return 1.0




def wind_to_risk(wind_kmph):


    if wind_kmph < 10:

        return 0.1
    

    if wind_kmph < 20:

        return 0.3
    

    if wind_kmph < 30:

        return 0.6
    

    return 1.0




def visibility_to_risk(visibility_km):


    if visibility_km > 8:

        return 0.1
    

    if visibility_km > 5:

        return 0.3
    

    if visibility_km > 2:

        return 0.6
    

    return 1.0




def slope_to_risk(slope_deg):


    if slope_deg < 2:

        return 0.1
    

    if slope_deg < 5:

        return 0.4
    

    if slope_deg < 8:

        return 0.7
    

    return 1.0


