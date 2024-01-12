from datetime import datetime, timedelta
from math import radians, sin, cos, sqrt, atan2
from operator import itemgetter

def convert_timestamp(timestamp):
    dt_object = datetime.utcfromtimestamp(timestamp)
    formatted_date = dt_object.strftime("%dth-%b, %H:%M")

    return formatted_date

def hours_between_timestamps(timestamp1, timestamp2):
    dt1 = datetime.utcfromtimestamp(timestamp1)
    dt2 = datetime.utcfromtimestamp(timestamp2)

    time_difference = dt2 - dt1

    total_hours = (time_difference.total_seconds() + 3600 - 1) // 3600

    return int(total_hours)

def current_timestamp_in_seconds():
    return int(datetime.now().timestamp())


def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the Haversine distance between two sets of latitude and longitude coordinates.
    """
    R = 6371  # Radius of the Earth in kilometers

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

def sort_parking_lots_by_distance(user_latitude, user_longitude, parking_lots):
    """
    Sort a list of parking lots based on their proximity to a user's coordinates.
    """
    for parking_lot in parking_lots:
        distance = haversine_distance(
            user_latitude, user_longitude,
            parking_lot.latitude, parking_lot.longitude
        )
        parking_lot.distance = distance

    sorted_parking_lots = sorted(parking_lots, key=itemgetter('distance'))
    return sorted_parking_lots

