from datetime import datetime


def get_today_datetime(hours: int = 0, minute: int = 0, seconds: int = 0):
    """
    Returns a datetime object for today with the specified time.
    Time complexity: O(1)
    Space complexity: O(1)
    :param hours:
    :param minute:
    :param seconds:
    :return:
    """
    today = datetime.today()
    return datetime(today.year, today.month, today.day, hours, minute, seconds)


def get_eod():
    """
    Returns a datetime object for the end of the day.
    Time complexity: O(1)
    Space complexity: O(1)
    :return:
    """
    today = datetime.today()
    return datetime(today.year, today.month, today.day, 23, 59, 59)
