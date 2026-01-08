from fastapi import APIRouter 
from typing import List
from src.controllers import appointment as appointment_controller
from src.models.appointment import AppointmentProposal, Appointment
from src.models.user import UserCreate, User
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

@router.post("/propose", status_code=200)
def propose_route(proposal: AppointmentProposal):
    return appointment_controller.propose(proposal)

@router.post("/confirm", status_code=201)
def confirm_route(appointment: Appointment):
    return appointment_controller.confirm(appointment)
