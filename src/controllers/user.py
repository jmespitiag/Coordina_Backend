from src.models.availability import Availability
from src.models.user import User
from src.services.storage_service import storage
from fastapi import HTTPException, Response
from src.services.calendar_service import generate_ics

#Controller functions for user routes

# Create a new user
def create_user(user: User):
    users = storage.load_users()


    if user.id is None:
        user.id = storage.generate_id()


    if any(u["id"] == user.id for u in users):
        raise HTTPException(status_code=400, detail="User already exists")

    users.append(user.model_dump())
    storage.save_users(users)
    return user

# Set or update a user's weekly availability
def set_availability(user_id: str, availability: Availability):

    #we get all users from our service
    users = storage.load_users()

    # Find the user by ID
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update the user's availability
    user["weekly_availability"] = availability.model_dump()

    storage.save_users(users)
    return availability

# Get a user's appointments
def get_appointments(user_id: str):

    users = storage.load_users()
    user_data = next((u for u in users if u["id"] == user_id), None)

    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_appointments_ids = user_data.get("appointments", [])
    print("user_appointments_ids:")
    print( user_appointments_ids )

    appointments = storage.load("appointments")
    print("appointments:")
    print( appointments )

    user_appointments = []

    for appointment in appointments:
        for id in user_appointments_ids:
            if appointment["id"] == id:
                user_appointments.append(appointment)

    print("user_appointments:")
    print( user_appointments )



    return user_appointments

# Get a user's calendar in ICS format
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



def get_all_users():
    print( "Loading all users..." )
    return storage.load_users()