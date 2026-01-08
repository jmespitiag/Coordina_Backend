from src.models.availability import Availability
from src.models.user import User
from src.services.storage_service import storage
from fastapi import HTTPException, Response
from src.services.calendar_service import generate_ics



def create_user(user: User):
    users = storage.load_users()

    # Generar id si no viene
    if user.id is None:
        user.id = storage.generate_id()

    # Verificar unicidad
    if any(u["id"] == user.id for u in users):
        raise HTTPException(status_code=400, detail="User already exists")

    users.append(user.model_dump())
    storage.save_users(users)
    return user

def set_availability(user_id: str, availability: Availability):
    users = storage.load_users()

    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user["weekly_availability"] = availability.model_dump()

    storage.save_users(users)
    return availability



def get_calendar(user_id: str):
    users = storage.load_users()
    user_data = next((u for u in users if u["id"] == user_id), None)
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_appointments_ids = user_data.get("appointments", [])

    appointments = storage.load("appointments")

    user_appointments = []

    for appointment in appointments:
        for id in user_appointments_ids:
            if appointment["id"] == id:
                user_appointments.append(appointment)


    ics_content = generate_ics(user_data, appointments)

    return Response(
        content=ics_content,
        media_type="text/calendar",
        headers={
            "Content-Disposition": "attachment; filename=schedule.ics"
        }
    )