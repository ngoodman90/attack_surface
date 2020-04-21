import datetime
from functools import wraps

from models import RequestStat


def timed_request(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        start_time = datetime.datetime.now()
        res = func(*args, **kwargs)
        end_time = datetime.datetime.now()
        RequestStat.create(
            start_time=start_time,
            end_time=end_time,
            diff=(end_time - start_time).microseconds,
        )
        return res

    return wrapped
