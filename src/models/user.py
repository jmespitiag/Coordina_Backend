from pydantic import BaseModel, Field
from typing import Optional, List
from src.models.appointment import Appointment
from uuid import uuid4


class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    appointments: Optional[List[Appointment]] = []

class UserCreate(BaseModel):
    name: str
    appointments: Optional[List[Appointment]] = []