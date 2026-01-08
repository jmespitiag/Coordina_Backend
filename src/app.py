from fastapi import FastAPI, HTTPException
from src.models.user import User
from datetime import time
from src.routes.user import router as user_router
from src.routes.appointment import router as appointment_router
from pathlib import Path


app = FastAPI(title='Schedule App')


app.include_router(user_router, prefix='/user', tags=["user"]) 
app.include_router(appointment_router, prefix='/appointment', tags=["appointment"])