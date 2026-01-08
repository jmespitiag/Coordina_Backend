from fastapi import APIRouter, HTTPException
from typing import List
from src.models.appointment import AppointmentProposal, Appointment
from src.services.storage_service import storage
from src.services.appointment_service import propose_appointments



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

def confirm(appointment: Appointment):
    # 1. Generar el ID para la nueva cita
    appointment.id = storage.generate_id()
    appointment_data = appointment.model_dump()

    appointment_data["date"] = storage._json_date_serializable(appointment_data["date"])
    # --- PARTE 1: Guardar en el archivo general de citas ---
    all_appointments = storage.load("appointments")
    all_appointments.append(appointment_data)
    storage.save("appointments", all_appointments)

    # --- PARTE 2: Actualizar a los usuarios involucrados ---
    all_users = storage.load("users")

    # Necesitamos al host y a los participantes
    ids_a_actualizar = set(appointment.participants_id)
    ids_a_actualizar.add(appointment.host_id)

    for user in all_users:
        if user["id"] in ids_a_actualizar:
            # Si el usuario no tiene la lista de appointments creada, la inicializamos
            if "appointments" not in user:
                user["appointments"] = []

            # Guardamos la cita dentro del usuario
            user["appointments"].append(appointment_data["id"])

    # Guardamos todos los usuarios con sus listas actualizadas
    storage.save("users", all_users)

    return appointment