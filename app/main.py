from fastapi import FastAPI, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from . import responses, database, ops



app = FastAPI()
@app.get("/")
async def greet():
    return {"hello": "world"}

@app.get('/GetAll')
async def get_all_hacks():
    return "all hacks"

@app.post("/login", tags=["login"])
async def login(login_deets:Request):
    infoDict = await login_deets.json()
    print(infoDict)
    email = infoDict['email']
    password = infoDict['password']
    # Verify credentials
    if await ops.verify_credentials(email, password):
        return responses.response(True, "logged in", {"email": email})
    else:
        raise HTTPException(401, "unauthorised login or email is wrong")


