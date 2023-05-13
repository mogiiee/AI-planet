from pydantic import BaseModel, constr, EmailStr
from datetime import datetime


class User(BaseModel):
    name: str
    email: str
    password: str
    hacks_created = []
    hacks_enlisted = []
    submissions = []


class Hackathon(BaseModel):
    title: str
    description: str
    email: EmailStr
    background_image: str
    hackathon_image: str
    submission_type: constr(regex="^(image|file|link)$")
    start_datetime: datetime
    end_datetime: datetime
    reward_prize: float


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class RegisterForHack(BaseModel):
    email: EmailStr
    hack_name: str


class Submissions(BaseModel):
    name: str
    which_hack: str
    submission_url: str
    summary: str
    email: EmailStr
    submission_type: constr(regex="^(link|picture|file)$")
