from pydantic import BaseModel,constr, EmailStr
from datetime import datetime


class User(BaseModel):
    name:str
    email: str
    password: str

class Hackathon(BaseModel):
    title: str
    description: str
    background_image: bytes
    hackathon_image: bytes
    submission_type: constr(regex="^(image|file|link)$")
    start_datetime: datetime
    end_datetime: datetime
    reward_prize: float

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str