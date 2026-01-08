from pydantic import BaseModel, field_validator
from datetime import time
from typing import List, Dict

DAYS = [
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday"
]


class TimeBlock(BaseModel):
    start: time
    end: time


class Availability(BaseModel):
    monday: List[TimeBlock] = []
    tuesday: List[TimeBlock] = []
    wednesday: List[TimeBlock] = []
    thursday: List[TimeBlock] = []
    friday: List[TimeBlock] = []
    saturday: List[TimeBlock] = []
    sunday: List[TimeBlock] = []

    def for_day(self, day: str) -> List[TimeBlock]:
        if day not in DAYS:
            raise ValueError(f"Invalid day: {day}")
        return getattr(self, day)
