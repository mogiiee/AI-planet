from fastapi import FastAPI, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from . import responses, database



app = FastAPI()
@app.get("/")
async def greet():
    return {"hello": "world"}

@app.get('/GetAll')
async def get_all_hacks():
    