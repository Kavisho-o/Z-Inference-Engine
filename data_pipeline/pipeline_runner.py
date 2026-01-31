'''


this pipeline converts raw synthetic segments into an ML-ready dataset


-> first we will generate multiple route using synthetic_route_generator.generate_multiple_routes()
and save it in a List[segment_dict]

-> then we will attach context to it (month, hour, weather, terrain, traffic proxy)

-> after this we will feature engineer this with engineer_features(segment)

-> then we will generate labels using
generate_risk_score(features)
risk_class_from_score(score)

-> finally we will save our datasets to 
raw: debugging and audits
processed: features only
final: training ready


'''



num_routes = 1,000
segments_per_route = 10
TOTAL_ROWS = 10,000



import random
import csv
import os
from datetime import datetime

from generators.synthetic_route_generator import generate_multiple_routes
from generators.weather_generator import generate_weather
from generators.road_terrain_generator import generate_road_terrain
from generators.traffic_proxy_generator import generate_traffic_risk

from processors.feature_engineering import engineer_features
from labelers.risk_labeler import generate_risk_score, risk_class_from_score



BASE_PATH = "data_pipeline/datasets"

RAW_PATH = os.path.join(BASE_PATH, "raw")
PROCESSED_PATH = os.path.join(BASE_PATH, "processed")
FINAL_PATH = os.path.join(BASE_PATH, "final")

for path in [RAW_PATH, PROCESSED_PATH, FINAL_PATH]:
    os.makedirs(path, exist_ok=True)




def sample_time():

    # samples random times

    month = random.randint(1, 12)
    hour = random.randint(0, 23)

    return month, hour



def run_pipeline(num_routes=1000,segments_per_route=10):
    
    # this is the main runner function


    print("~~~~~~~~~~~~~~~~Starting ZEPHYR data pipeline~~~~~~~~~~~~~~~~")


    segments = generate_multiple_routes(

        num_routes=num_routes,
        segments_per_route=segments_per_route

    )


    raw_rows = []
    processed_rows = []
    final_rows = []


    for segment in segments:


        month, hour = sample_time()


        weather = generate_weather(segment, month, hour)

        terrain = generate_road_terrain(segment)

        traffic = generate_traffic_risk(

            terrain["road_type"],
            hour,
            weather["rain_intensity"]

        )


        # attach everything to raw segment

        segment.update(

            {
            **weather,
            **terrain,
            "traffic_risk_index": traffic,
            "month": month,
            "hour": hour
            }

        )

        raw_rows.append(segment.copy())


        # feature engineering

        features = engineer_features(segment)
        processed_rows.append(features.copy())

        # label generation

        risk_score = generate_risk_score(features)
        risk_class = risk_class_from_score(risk_score)


        final_row = {

            **features,
            "risk_score": risk_score,
            "risk_class": risk_class

        }


        final_rows.append(final_row)



    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")


    save_csv(raw_rows, RAW_PATH, f"raw_segments_{timestamp}.csv")
    save_csv(processed_rows, PROCESSED_PATH, f"processed_features_{timestamp}.csv")
    save_csv(final_rows, FINAL_PATH, f"final_dataset_{timestamp}.csv")


    print("~~~~~~~~~~~~~~~~Pipeline completed successfully~~~~~~~~~~~~~~~~")



def save_csv(rows, folder, filename):

    if not rows:
        return
    

    path = os.path.join(folder, filename)
    keys = rows[0].keys()


    with open(path, "w", newline="", encoding="utf-8") as f:

        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(rows)


    print(f"~~~~~~~~~~~~~~~~ Saved {len(rows)} rows -> {path} ~~~~~~~~~~~~~~~~")




if __name__ == "__main__":

    run_pipeline()
