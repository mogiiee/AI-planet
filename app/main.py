from fastapi import FastAPI, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from . import responses, database, ops, models
import copy
from app.auth.jwt_bearer import JWTBearer
from app.auth.jwt_handler import signJWT




app = FastAPI()
@app.get("/")
async def greet():
    return {"hello": "world"}

@app.get('/GetAll')
async def get_all_hacks():
    return "all hacks"

@app.post("/login", tags=["auth"])
async def login(login_details: models.UserLoginSchema):
    infoDict =jsonable_encoder(login_details) 
    print(infoDict)
    email = infoDict['email']
    password = infoDict['password']
    # Verify credentials
    if await ops.verify_credentials(email, password):
        return responses.response(True, "logged in", {"email": email})
    else:
        raise HTTPException(401, "unauthorised login or email is wrong")

@app.post("/signup", tags=["auth"])
async def signup(signup_details: models.User):
    infoDict = jsonable_encoder(signup_details) 
    print(infoDict)
    infoDict = dict(infoDict)
    # Checking if email already exists
    email_count = database.user_collection.count_documents(
        {"email": infoDict["email"]}
    )
    if email_count > 0:
        return responses.response(False, "duplicated user, email already in use", None)
    # Insert new user

    encoded_password = ops.hash_password(str(infoDict["password"]))
    infoDict['password'] = encoded_password
    print(infoDict)
    json_signup_details = jsonable_encoder(infoDict)
    await ops.inserter(json_signup_details)
    return responses.response(True, "inserted", 
        infoDict
    )

@app.post("/user/add_hack", dependencies=[Depends(JWTBearer())],tags=["add hack"])
async def add_hack(hack_deets: models.Hackathon):
    infoDict = jsonable_encoder(hack_deets)
    json_hack_deets = dict(infoDict)
    email = infoDict['email']
    full_profile = await ops.full_user_data(email)
    creator_user_attributes = full_profile["creator_attributes_jobs"]
    original_attributes = copy.deepcopy(full_profile["creator_attributes_jobs"])
    creator_user_attributes.append(json_hack_deets)
    print(creator_user_attributes)
    ops.creator_attributes_jobs_updater(infoDict["email"],creator_user_attributes)
    ops.hack_inserter(json_hack_deets)
    return responses.response(True, "job posted!", infoDict)

@app.get("/all-users")
async def Get_all_data():
    try:
        response = ops.get_all_data()
        return responses.response(True, None, str(response))
    except Exception as e:
        return responses.response(False, str(e),"something went wrong please try again")