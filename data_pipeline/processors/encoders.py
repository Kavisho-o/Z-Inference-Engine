'''


using ordinal encoding rather than one hot because ordinal encoding is better for tree
models (my current thought says im going to use random forest, im not sure though, will come back to this)

moutain road have the highest risk ordinal, this is intentional


'''



ROAD_TYPE_ENCODING = {

    "highway": 1,
    "rural": 2,
    "city": 3,
    "mountain": 4

}



TERRAIN_ENCODING = {

    "flat": 1,
    "hilly": 2,
    "mountainous": 3

}



def encode_road_type(road_type):

    return ROAD_TYPE_ENCODING.get(road_type, 2)




def encode_terrain(terrain_type):

    return TERRAIN_ENCODING.get(terrain_type, 2)

  

