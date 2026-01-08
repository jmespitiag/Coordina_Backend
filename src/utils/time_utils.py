def time_to_minutes(t):
    if isinstance(t, str):
        h, m = map(int, t.split(":"))
        return h * 60 + m
    return t.hour * 60 + t.minute


def minutes_to_time(m):
    return f"{m//60:02d}:{m%60:02d}"
