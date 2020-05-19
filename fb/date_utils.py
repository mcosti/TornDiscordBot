from datetime import datetime
import pytz

torn_tz = pytz.timezone("Zulu")


def datetime_from_torn(timestamp):
    return datetime.fromtimestamp(timestamp, torn_tz)


def torn_now_datetime():
    return datetime.now(tz=torn_tz)


def torn_now_timestamp():
    return int(torn_now_datetime().timestamp())
