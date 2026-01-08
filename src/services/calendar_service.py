from ics import Calendar, Event
from datetime import datetime

def generate_ics(user, appointments):
    calendar = Calendar()

    for appt in appointments:
        event = Event()
        event.name = appt["title"]
        event.begin = datetime.fromisoformat(
            f"{appt['date']}T{appt['start']}"
        )
        event.end = datetime.fromisoformat(
            f"{appt['date']}T{appt['end']}"
        )
        event.location = appt.get("location")
        event.uid = appt["id"]

        calendar.events.add(event)

    return str(calendar)