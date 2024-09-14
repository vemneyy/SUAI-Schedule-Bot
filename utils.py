# utils.py

from datetime import datetime, timedelta
from functools import wraps

DAY_OF_WEEK_MAPPING = {
    "Monday": "Понедельник",
    "Tuesday": "Вторник",
    "Wednesday": "Среда",
    "Thursday": "Четверг",
    "Friday": "Пятница",
    "Saturday": "Суббота",
    "Sunday": "Воскресенье"
}


# Определение четности недели
def is_odd_week():
    week_number = datetime.now().isocalendar()[1]
    return "even" if week_number % 2 != 0 else "odd"


# Декоратор для ограничения запросов
def rate_limit(limit: int, time_window: timedelta):
    user_requests = {}

    def decorator(func):
        @wraps(func)
        async def wrapper(message, *args, **kwargs):
            user_id = message.from_user.id
            now = datetime.now()

            if user_id in user_requests:
                request_times = user_requests[user_id]
                user_requests[user_id] = [time for time in request_times if now - time < time_window]
            else:
                user_requests[user_id] = []

            if len(user_requests[user_id]) < limit:
                user_requests[user_id].append(now)
                return await func(message, *args, **kwargs)
            else:
                return

        return wrapper

    return decorator
