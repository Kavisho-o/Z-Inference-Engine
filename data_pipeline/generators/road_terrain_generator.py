'''

This module decides what kind of road the segment is on and what terrain it crosses.


FEATURES:

road_type: highway, city, rural, mountain
elevation (meters)
terrain_type: flat, hilly, mountainous
slope (derived)


ELEVATION LOGIC:
< 200 m → plains
200 to 600 m → hilly
> 600 m → mountainous

ROAD BIAS:
Mountain terrain -> mountain roads likely
Urban plains -> city roads
Long routes -> highways more likely


'''



import random



def generate_elevation(lat):

    # generates elevation in meters based on latitude


    if lat > 28:                               # himalayan region

        return random.uniform(800, 3500)
    
    
    elif lat > 23:

        return random.uniform(300, 1200)
    

    else:

        return random.uniform(0, 400)
    

def get_terrain_type(elevation):


    if elevation < 200:

        return "flat"
    

    elif elevation < 600:

        return "hilly"
    

    else:

        return "mountainous"
    

def generate_slope(terrain_type):


    # slope simulates road steepness

    if terrain_type == "flat":

        return round(random.uniform(0, 2), 2)
    

    elif terrain_type == "hilly":

        return round(random.uniform(2, 6), 2)
    
    
    else:

        return round(random.uniform(6, 15), 2)
    


def generate_road_type(terrain_type, segment_length_km):


    if terrain_type == "mountainous":

        return random.choices(
            ["mountain", "rural"],
            weights=[0.7, 0.3]
        )[0]
    

    if segment_length_km > 20:

        return "highway"


    return random.choices(
        ["city", "rural", "highway"],
        weights=[0.5, 0.3, 0.2]
    )[0]




def generate_road_terrain(segment):

    # this is the core function which encapsulates everything and generates a final road terrain

    lat = segment["start_lat"]
    seg_len = segment["segment_length_km"]


    elevation = generate_elevation(lat)
    terrain_type = get_terrain_type(elevation)
    slope = generate_slope(terrain_type)
    road_type = generate_road_type(terrain_type, seg_len)


    return {
        "elevation": round(elevation, 1),            
        "terrain_type": terrain_type,              
        "slope": slope,                              
        "road_type": road_type                       
    }




sample_segment = {"start_lat": 30.5, "segment_length_km": 8}
print(generate_road_terrain(sample_segment))










