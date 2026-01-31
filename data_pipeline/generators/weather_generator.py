'''


This module assigns realistic, India-specific weather to each route segment.



India Climate Heuristics (for reference)

Monsoon (Jun to Sep):
High rain
Lower visibility
Moderate winds

Summer (Mar to May):
High temperature
Dust → reduced visibility
Occasional wind

Winter (Dec to Feb):
Low temp (especially north)
Fog → low visibility
Low rain

Latitude effect:
North India → colder winters
South India → warmer year-round



'''





import random



def is_monsoon(month):

    # is it monsoon?

    return 6 <= month <= 9




def generate_temperature(lat, month):

    # generates realistic temperature based on latitude and month (in degree celsius)


    base_temp = 30 if lat < 23 else 25  # south hotter than north


    if month in [12, 1, 2]:                            # winter

        temp = base_temp - random.uniform(8, 12)


    elif month in [3, 4, 5]:                           # summer

        temp = base_temp + random.uniform(5, 10)


    elif month in [6, 7, 8, 9]:                        # monsoon

        temp = base_temp + random.uniform(0, 4)


    else:                                              # post-monsoon

        temp = base_temp + random.uniform(2, 5)


    return round(temp, 1)




def generate_rain(month):

    # generates rainfall (monsoom dominant)


    if is_monsoon(month):

        return round(random.uniform(2, 20), 2)        # mm per hour
    

    elif month in [10, 11]:

        return round(random.uniform(0, 5), 2)
    

    else:

        return round(random.uniform(0, 2), 2)





def generate_wind(month):

    # generates wind speed


    if is_monsoon(month):

        return round(random.uniform(10, 40), 1)      # km per hour
    

    else:

        return round(random.uniform(2, 20), 1)
    



def generate_visibility(rain_intensity, is_night):

    # generates visibility (affected by rain and night time)

    visibility = random.uniform(5, 12)             # km


    if rain_intensity > 5:

        visibility -= random.uniform(2, 5)



    if is_night:

        visibility -= random.uniform(1, 3)



    return round(max(visibility, 0.5), 1)






def generate_weather(segment, month, hour):

    # this is the main function that the pipeline will call
    # this will attach the weather data to a route segment


    lat = segment["start_lat"]
    is_night = hour < 6 or hour > 18


    rain = generate_rain(month)
    wind = generate_wind(month)
    temp = generate_temperature(lat, month)
    visibility = generate_visibility(rain, is_night)


    weather_data = {

        "rain_intensity": rain,
        "wind_speed": wind,
        "temperature": temp,
        "visibility": visibility

    }


    return weather_data






sample_segment = {"start_lat": 28.6}
print(generate_weather(sample_segment, month=7, hour=22))





























