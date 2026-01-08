from pydantic import BaseModel
from typing import List
from datetime import date, time
from typing import Optional

class Appointment(BaseModel):
    id: Optional[str] = None
    title: str
    date: date
    week: int
    start: time
    end: time
    host_id: str
    participants_id: List[str]
    location: Optional[str] = None


class AppointmentProposal(BaseModel):
    title: str
    participants_id: List[str]
    week: int
    duration_minutes: int
    day: Optional[List[str]] = None
    location: Optional[str] = None