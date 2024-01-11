from datetime import datetime, timedelta

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
