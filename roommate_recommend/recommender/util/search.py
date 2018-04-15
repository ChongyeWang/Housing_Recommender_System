import geopy.distance

def get_satisfied_house(houses_list, user_location, distance_range):
    """return a list of houses in the distance range"""
    satisfied_house_list = []
    for house in houses_list:
        distance = geopy.distance.vincenty((user_name[lat], user_name[lon]), (house[lat], house[lon])).m
        if distance <= distance_range: satisfied_house_list.append(house)
    return satisfied_house_list
