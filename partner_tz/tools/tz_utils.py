# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from datetime import date, datetime

import pytz

UTC_TZ = pytz.timezone("UTC")


def tz_to_tz_naive_datetime(from_tz, to_tz, date_time):
    """
    Convert tz-naive datetime from a specifc tz to a tz-naive datetime of a specific tz

    :param from_tz: pytz.timezone object or tz selection value
    :param to_tz: pytz.timezone object or tz selection value
    :param date_time: tz-naive datetime.datetime object
    :return: tz-naive datetime.datetime object
    """
    if isinstance(from_tz, str):
        from_tz = pytz.timezone(from_tz)
    if isinstance(to_tz, str):
        to_tz = pytz.timezone(to_tz)
    return from_tz.localize(date_time).astimezone(to_tz).replace(tzinfo=None)


def tz_to_utc_naive_datetime(from_tz, date_time):
    return tz_to_tz_naive_datetime(from_tz, UTC_TZ, date_time)


def utc_to_tz_naive_datetime(to_tz, date_time):
    return tz_to_tz_naive_datetime(UTC_TZ, to_tz, date_time)


def tz_to_tz_time(from_tz, to_tz, time, base_date=None):
    """
    Convert datetime.time from a specific tz to a datetime.time of a specific tz

    :param from_tz: pytz.timezone object or tz selection value
    :param to_tz: pytz.timezone object or tz selection value
    :param time: datetime.time object
    :param base_date: OPTIONAL datetime.date or datetime.datetime object to use
           for the conversion
    :return: datetime.time object
    """
    # Combine time with a date
    if base_date is None:
        base_date = date.today()
    date_time = datetime.combine(base_date, time)
    new_date_time = tz_to_tz_naive_datetime(from_tz, to_tz, date_time)
    return new_date_time.time()


def tz_to_utc_time(from_tz, time, base_date=None):
    return tz_to_tz_time(from_tz, UTC_TZ, time, base_date=base_date)


def utc_to_tz_time(to_tz, time, base_date=None):
    return tz_to_tz_time(UTC_TZ, to_tz, time, base_date=base_date)
