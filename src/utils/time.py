from datetime import datetime


def get_today_datetime(hours: int = 0, minute: int = 0, seconds: int = 0):
    today = datetime.today()
    return datetime(today.year, today.month, today.day, hours, minute, seconds)


def get_eod():
    today = datetime.today()
    return datetime(today.year, today.month, today.day, 23, 59, 59)
