'''

generating risk labels, specifically:
risk_score -> continuous [0 to 100]
risk_class -> safe / moderate / dangerous

weight table

| Component       | Weight   |
| --------------- | -------- |
| rain_risk       | 0.18     |
| visibility_risk | 0.16     |
| wind_risk       | 0.08     |
| slope_risk      | 0.12     |
| traffic_risk    | 0.18     |
| terrain penalty | 0.08     |
| road penalty    | 0.06     |
| night penalty   | 0.08     |
| monsoon penalty | 0.06     |
| TOTAL           | 1.00     |


thought process behind this:

- weather dominates in india
- traffic is highly proportionla to rain
- terrain and roads are secondary (relatively) 
- night and monsoon are just basic amplifiers


PENALTIES:

Terrain Penalty
flat -> 0.0
hilly -> 0.5
mountainous -> 1.0

Road Penalty
highway -> 0.0
rural -> 0.4
city -> 0.6
mountain -> 1.0


'''


def terrain_penalty(terrain_enc):


    if terrain_enc == 1:          # flat
        
        return 0.0
    

    if terrain_enc == 2:          # hilly
        
        return 0.5
    

    return 1.0                    # mountainous




def road_penalty(road_enc):


    if road_enc == 1:             # highway
       
        return 0.0
    

    if road_enc == 2:             # rural
       
        return 0.4
    

    if road_enc == 3:             # city
        
        return 0.6
    

    return 1.0                    # mountain




def generate_risk_score(features):

    # input: engineered feature dict
    # output: risk_score in range [0,100]


    score = 0.0


    score += 0.18 * features["rain_risk"]

    score += 0.16 * features["visibility_risk"]

    score += 0.08 * features["wind_risk"]

    score += 0.12 * features["slope_risk"]

    score += 0.18 * (features["traffic_risk_index"] / 100)

    score += 0.08 * terrain_penalty(features["terrain_enc"])

    score += 0.06 * road_penalty(features["road_type_enc"])

    score += 0.08 * features["night_flag"]

    score += 0.06 * features["monsoon_flag"]


    return round(score * 100, 2)


def risk_class_from_score(score):


    if score < 30:

        return "Safe"
    

    if score < 60:

        return "Moderate"
    

    return "Dangerous"






'''

this may seem very abstract BUT that is very intentional
this is a weak teacher that encodes domain intuition.
tree models learn non-linear corrections over this heuristic,
which is why the final model outperforms the rule-based system


'''