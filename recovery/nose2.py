from datetime import time, datetime, timedelta
from typing import List, Tuple


# convierte time a minutos desde medianoche



def time_to_min(t: time) -> int:
    return t.hour * 60 + t.minute




def min_to_time(m: int) -> time:
    h = m // 60
    mm = m % 60
    return time(hour=h, minute=mm)




# recibe listas de intervalos en minutos [(s,e), ...] y devuelve intersección


def intersect_intervals(lists: List[List[Tuple[int,int]]]) -> List[Tuple[int,int]]:
    if not lists:
        return []
        # empezamos con los intervalos del primer usuario
    result = lists[0]
    for lst in lists[1:]:
        new_res = []
        for a_start, a_end in result:
            for b_start, b_end in lst:
                s = max(a_start, b_start)
                e = min(a_end, b_end)
                if s + 1 <= e:
                    new_res.append((s, e))
                    result = new_res
                if not result:
                    break
    return result




# fragmenta intervalos para que cumplan con una duracion minima (en minutos)


def split_intervals_for_duration(intervals: List[Tuple[int,int]], duration_min: int) -> List[Tuple[int,int]]:
    out = []
    for s, e in intervals:
        cur = s
        while cur + duration_min <= e:
            out.append((cur, cur + duration_min))
            cur += 15 # paso de 15 minutos (configurable)
    return out