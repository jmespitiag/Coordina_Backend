from typing import List, Tuple
from datetime import date, time
from src.services.storage_service import load_availability, load_user, load_appointment
from src.utils.time_utils import time_to_min, min_to_time, intersect_intervals, split_intervals_for_duration
from src.models.availability import DayInterval


WEEKDAYS = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']




def get_user_daily_intervals(user_id: str, weekday: str) -> List[Tuple[int,int]]:
    avail = load_availability(user_id)
    if not avail:
        return []
    day_list = getattr(avail, weekday, [])
    out = []
    for di in day_list:
        if isinstance(di, dict):
            # cuando viene desde JSON
            start = time_to_min(time.fromisoformat(di['start']))
            end = time_to_min(time.fromisoformat(di['end']))
        elif isinstance(di, DayInterval):
            start = time_to_min(di.start)
            end = time_to_min(di.end)
        else:
            # pydantic model
            start = time_to_min(di.start)
            end = time_to_min(di.end)
            out.append((start, end))
    return out




def find_common_slots(participants: List[str], weekday: str, duration_minutes: int) -> List[Tuple[time,time]]:
    # recolectar intervalos de cada participante para el dia
    lists = [get_user_daily_intervals(uid, weekday) for uid in participants]
    # intersectar
    common = intersect_intervals(lists)
    # dividir por duración
    slots = split_intervals_for_duration(common, duration_minutes)
    # convertir a time
    return [(min_to_time(s), min_to_time(e)) for s, e in slots]