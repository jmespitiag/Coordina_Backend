# src/services/appointment_service.py

from datetime import time
from src.services.storage_service import storage
from datetime import date, timedelta, datetime
from src.utils.time_utils import time_to_minutes, minutes_to_time

DAYS = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]

def get_appointments_for_user_and_week(user_id: str, week: int, year: int = 2026):
    appointments = storage.load("appointments")
    result = []

    for appt in appointments:
        if user_id not in appt["participants_id"]:
            continue

        appt_date = date.fromisoformat(appt["date"])
        iso_year, iso_week, _ = appt_date.isocalendar()

        if iso_week == week and iso_year == year:
            result.append(appt)

    return result

def subtract_block(free_start, free_end, busy_start, busy_end):
    """
    Todos los intervalos como [start, end)
    en minutos
    """
    fs = time_to_minutes(free_start)
    fe = time_to_minutes(free_end)
    bs = time_to_minutes(busy_start)
    be = time_to_minutes(busy_end)

    # No intersección
    if be <= fs or bs >= fe:
        return [(free_start, free_end)]

    # Busy cubre todo
    if bs <= fs and be >= fe:
        return []

    result = []

    if bs > fs:
        result.append((minutes_to_time(fs), minutes_to_time(bs)))

    if be < fe:
        result.append((minutes_to_time(be), minutes_to_time(fe)))

    return result

def get_effective_availability(
    weekly_availability,
    appointments,
    day_name
):
    blocks = [
        (slot["start"], slot["end"])
        for slot in weekly_availability.get(day_name, [])
    ]

    for appt in appointments:
        appt_date = date.fromisoformat(appt["date"])
        appt_day = DAYS[appt_date.weekday()]

        if appt_day != day_name:
            continue

        busy_start = appt["start"][:5]
        busy_end = appt["end"][:5]

        new_blocks = []
        for free_start, free_end in blocks:
            new_blocks.extend(
                subtract_block(
                    free_start, free_end,
                    busy_start, busy_end
                )
            )

        blocks = new_blocks

    return blocks

def get_date_from_week(week: int, weekday: int, year: int):
    first_day = date.fromisocalendar(year, week, 1)
    return first_day + timedelta(days=weekday)

def split_block(start: str, end: str, duration):
    slots = []
    fmt = "%H:%M"

    # Si duration es un objeto time (ej. 00:30:00), conviértelo a minutos
    if hasattr(duration, 'hour'):
        duration_mins = duration.hour * 60 + duration.minute
    else:
        duration_mins = int(duration)

    current = datetime.strptime(start, fmt)
    end_dt = datetime.strptime(end, fmt)

    # Usa duration_mins en lugar de duration
    while current + timedelta(minutes=duration_mins) <= end_dt:
        slot_end = current + timedelta(minutes=duration_mins)
        slots.append({
            "start": current.strftime(fmt),
            "end": slot_end.strftime(fmt)
        })
        current = slot_end

    return slots


def propose_appointments(
    participants_id: list[str],
    week: int,
    duration: int,
    location: str | None,
    days: list[str] | None = None,
    title: str | None = None,
    year: int = 2026
):
    users = storage.load_users()
    host_id = participants_id[0]

    selected_days = days if days else DAYS

    # 🧱 Disponibilidad efectiva por usuario
    weekly_blocks_per_user = []

    for user_id in participants_id:
        user = next(u for u in users if u["id"] == user_id)
        availability = user.get("weekly_availability")

        if not availability:
            raise ValueError(f"User {user_id} has no weekly availability")

        user_appointments = get_appointments_for_user_and_week(
            user_id, week, year
        )

        effective_week = {}

        for day in selected_days:
            if day not in DAYS:
                continue

            if not user_appointments:
                effective_week[day] = [
                    (slot["start"], slot["end"])
                    for slot in availability.get(day, [])
                ]
            else:
                effective_week[day] = get_effective_availability(
                    availability,
                    user_appointments,
                    day
                )

        weekly_blocks_per_user.append(effective_week)

    # 🧠 Intersección entre usuarios
    results = {}

    for day in selected_days:
        if day not in DAYS:
            continue

        day_blocks = []

        for user_week in weekly_blocks_per_user:
            blocks = set(user_week.get(day, []))
            day_blocks.append(blocks)

        common_blocks = set.intersection(*day_blocks) if day_blocks else set()

        idx = DAYS.index(day)
        date_real = get_date_from_week(week, idx, year).isoformat()
        day_slots = []

        for start, end in common_blocks:
            chunks = split_block(start, end, duration)
            for c in chunks:
                day_slots.append({
                    "title": title,
                    "date": date_real,
                    "start": c["start"],
                    "end": c["end"],
                    "host_id": host_id,
                    "participants_id": participants_id,
                    "location": location
                })

        results[day] = day_slots

    return results



