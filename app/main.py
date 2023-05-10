from fastapi import FastAPI, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from . import responses, database, ops, models



app = FastAPI()
@app.get("/")
async def greet():
    return {"hello": "world"}

@app.get('/GetAll')
async def get_all_hacks():
    return "all hacks"

@app.post("/login", tags=["auth"])
async def login(login_details: models.User):
    infoDict = await login_details.json()
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
    infoDict = await signup_details.json()
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

@app.post("/creator/add_job", tags=["creator"])
async def add_job(job_deets: Request):
    infoDict = await job_deets.json()
    json_job_deets = dict(infoDict)
    email = infoDict['email']
    full_profile = await ops.find_user_email(email)
    creator_user_attributes = full_profile["creator_attributes_jobs"]
    original_attributes = copy.deepcopy(full_profile["creator_attributes_jobs"])
    creator_user_attributes.append(json_job_deets)
    print(creator_user_attributes)
    ops.creator_attributes_jobs_updater(infoDict["email"],creator_user_attributes)
    ops.job_inserter(json_job_deets)
    return responses.response(True, "job posted!", infoDict)
