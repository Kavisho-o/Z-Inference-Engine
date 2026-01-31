'''

traffic_proxy_generator.py generates a derived congestion & operational risk signal
this signal will be fed to the ml model and used in SHAP explanations later

this module will generate a traffic_risk_index -> 0 to 100
higher traffic_risk_index will mean more congestion, higher delay probability & higher accident likelihood

traffic_risk_index dependencies:

1. Road Type : city=60, highway=30, rural=25, mountain=40
2. Time of Day : rush hours (8 to 10, 17 to 20) = more risk
3. Weather Impact : rain increases congestion (heavy rain will amplify this)
4. Urban Bias : this elevates everything else

final value is clamped to [0,100]


'''




import random



BASE_ROAD_RISK = {

    "city": 60,
    "highway": 30,
    "rural": 25,
    "mountain": 40

}



def time_risk_multiplier(hour):


    if 8 <= hour <= 10 or 17 <= hour <= 20:

        return 1.4                            # rush hour
    
    if hour >= 22 or hour <= 5:

        return 0.7                            # low traffic
    
    return 1.0



def weather_risk_addition(rain_intensity):


    if rain_intensity > 10:

        return 20
    
    
    elif rain_intensity > 5:

        return 10
    
    
    elif rain_intensity > 1:

        return 5
    

    return 0




def generate_traffic_risk(road_type, hour, rain_intensity):

    # core function encapsulating everything else and generating the final traffic_risk_index

    base = BASE_ROAD_RISK.get(road_type, 30)

    risk = base * time_risk_multiplier(hour)
    risk += weather_risk_addition(rain_intensity)

   
    risk += random.uniform(-5, 5)                   # small randomness for realism

    return int(max(0, min(100, risk)))




"""

there is a concern im having with these traffic conditions being too loose
there is a slight chance that it will keep generating 100 traffic too often, the question is
“will the model keep seeing 100 even when the situation is bad-but-not-maximally-bad?”
we will come onto this later and fix it if it is actually a concern


"""




