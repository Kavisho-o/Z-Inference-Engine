'''

This module creates synthetic journey routes and splits them into segments across India.

Why? 
-> We need to simulate realistic routes across India without calling any map APIs.

'''



import random
import math
import uuid       # for creating unique ids for each route 



# India's approximate bounding box

INDIA_BOUNDS = {

    "lat_min": 8.0,
    "lat_max": 37.0,
    "lon_min": 68.0,
    "lon_max": 97.0

}



def random_coordinate():

    # sample a random lat/lon within India's bounds

    lat = random.uniform(INDIA_BOUNDS["lat_min"], INDIA_BOUNDS["lat_max"])
    lon = random.uniform(INDIA_BOUNDS["lon_min"], INDIA_BOUNDS["lon_max"])

    return lat, lon



def haversine_distance(lat1, lon1, lat2, lon2):

    # computing distance between two lat/lon points in kms

    R = 6371  # earth radius in km

    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2

    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))




def generate_route(num_segments=10):

    # generate a synthetic route across india split into segments. 
    # this function returns a list of segment dictionaries.

    route_id = str(uuid.uuid4())      # creating unique ids for every route (to avoid clashing and ensuring safety)

    start_lat, start_lon = random_coordinate()
    end_lat, end_lon = random_coordinate()

    total_distance = haversine_distance(start_lat, start_lon, end_lat, end_lon)

    segments = []

    for i in range(num_segments):

        frac_start = i / num_segments
        frac_end = (i + 1) / num_segments

        seg_start_lat = start_lat + (end_lat - start_lat) * frac_start
        seg_start_lon = start_lon + (end_lon - start_lon) * frac_start

        seg_end_lat = start_lat + (end_lat - start_lat) * frac_end
        seg_end_lon = start_lon + (end_lon - start_lon) * frac_end

        seg_length = haversine_distance(seg_start_lat, seg_start_lon, seg_end_lat, seg_end_lon)

        segments.append({

            "route_id": route_id,                         # unique id per journey
            "segment_id": i,                              # index of the segment within the route
            "start_lat": seg_start_lat,                   # segment start lat
            "start_lon": seg_start_lon,                   # segment start lon
            "end_lat": seg_end_lat,                       # segment end lat
            "end_lon": seg_end_lon,                       # segment end lon
            "segment_length_km": seg_length,              # distance of segment 
            "total_route_length_km": total_distance       # full route length

        })

    return segments




def generate_multiple_routes(num_routes=1000, segments_per_route=10):

    # generate multiple synthetic routes

    all_segments = []

    for _ in range(num_routes):
        
        route_segments = generate_route(segments_per_route)
        all_segments.extend(route_segments)

    return all_segments
