from fastapi import APIRouter 
from typing import List
from src.controllers import user as user_controller
from src.models.availability import Availability
from src.models.user import UserCreate, User

router = APIRouter()


@router.post('/create', status_code=201)
def create_user(user: UserCreate):
    new_user = User(**user.model_dump())

    return user_controller.create_user(new_user)

@router.put("/{user_id}/availability")
def update_availability(user_id: str, availability: Availability):
    return user_controller.set_availability(user_id, availability)

@router.get("/users/{user_id}/calendar")
def get_calendar(user_id: str):
    return user_controller.get_calendar(user_id)

@router.get("/users", response_model=List[User])
def get_all_users_route():
    return user_controller.get_all_users()  