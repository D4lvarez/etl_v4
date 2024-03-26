import calendar
from datetime import datetime, timedelta


def get_last_day_of_month(month: int, year: int) -> str:
    last_day = calendar.monthrange(year, month)[1]
    return f"{year}-{month}-{last_day}"


def get_next_day() -> str:
    date_object = datetime.now()
    result = date_object + timedelta(days=1)
    return result.strftime("%Y-%m-%d")
