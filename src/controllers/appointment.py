from fastapi import APIRouter, HTTPException
from typing import List
from src.models.appointment import AppointmentProposal, Appointment
from src.services.storage_service import storage
from src.services.appointment_service import propose_appointments


# Controller functions for appointment routes


# Propose appointment slots based on participants' availability

def propose(proposal: AppointmentProposal):
    try:
        slots = propose_appointments(
            proposal.participants_id,
            proposal.week,
            proposal.duration_minutes,
            proposal.location,
            proposal.day,
            proposal.title

        )
        return {"available_slots": slots}
    except StopIteration:
        raise HTTPException(status_code=404, detail="User or availability not found")
    

# Confirm and save an appointment after being chosen and accepted 
def confirm(appointment: Appointment):
   #Generate id for the appointment
    appointment.id = storage.generate_id()
    appointment_data = appointment.model_dump()

    appointment_data["date"] = storage._json_date_serializable(appointment_data["date"])
    #Part 1 : Save the appointment itself
    all_appointments = storage.load("appointments")
    all_appointments.append(appointment_data)
    storage.save("appointments", all_appointments)

            # --- PART 2: Update the involved users ---
    all_users = storage.load("users")

    # We need to update both the host and the participants
    ids_a_actualizar = set(appointment.participants_id)


    for user in all_users:
        if user["id"] in ids_a_actualizar:
            # If the user does not have the appointments list created, initialize it
            if "appointments" not in user:
                user["appointments"] = []

            # Save the appointment within the user
            user["appointments"].append(appointment_data["id"])

    # Save all users with their updated appointment lists
    storage.save("users", all_users)

    return appointment