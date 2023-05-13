from fastapi import FastAPI, HTTPException, Depends, File, UploadFile, Form
from fastapi.encoders import jsonable_encoder
from . import responses, database, ops, models,exporter
from datetime import datetime
from app.auth.jwt_bearer import JWTBearer
from app.auth.jwt_handler import signJWT
import pyrebase
import json
from firebase_admin import credentials, storage
import firebase_admin



app = FastAPI()

firebase = pyrebase.initialize_app(database.firebaseConfig)
storage = firebase.storage()
storage.child
cred = credentials.Certificate("ai-planet-firebase-adminsdk-g7a8x-65b9193f00.json")

firebase_admin.initialize_app(
    cred, {"storageBucket": "gs://ai-planet.appspot.com"}
)


@app.get("/")
async def greet():
    return {"hello": "people from AI planet"}

@app.get("/GetAllHacks")
async def Get_all_hacks():
    metadata = ops.get_all_hacks()
    for x in metadata:
        del x["_id"]
    return responses.response(True,None, metadata)


@app.post("/login", tags=["auth"])
async def login(login_details: models.UserLoginSchema):
    infoDict =jsonable_encoder(login_details) 
    print(infoDict)
    email = infoDict['email']
    password = infoDict['password']
    # Verify credentials
    if await ops.verify_credentials(email, password):
        return responses.response(True, "logged in", signJWT(infoDict))
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
    return responses.response(True, "inserted",signJWT(infoDict)
    )

@app.post("/user/add_hack", dependencies=[Depends(JWTBearer())],tags=["hack"])
async def add_hack(hack_deets: models.Hackathon):
    infoDict = jsonable_encoder(hack_deets)
    json_hack_deets = dict(infoDict)
    email = infoDict['email']
    hack_name = json_hack_deets["title"]
    # print(hack_name)
    all_hacks = ops.get_all_hacks()
    # print(all_hacks)
    for x in all_hacks:
        print(x["title"])
        if hack_name == x["title"]:
            return responses.response(False, "hack already exists try a different name", hack_name )
        else:
            continue
    if ops.email_finder(email):
        full_profile = await ops.full_user_data(email)
        user_hacks_created = full_profile["hacks_created"]
        # original_attributes = copy.deepcopy(full_profile["creator_attributes_jobs"])
        user_hacks_created.append(json_hack_deets)
        ops.user_hack_created_updater(infoDict["email"],user_hacks_created )
        ops.hack_inserter(json_hack_deets)
        return responses.response(True, "hack posted!", infoDict)
    else:
        return responses.response(False, "email does not exist", email) 


@app.get("/all-users", tags=["helpers"])
async def Get_all_data():
    try:
        response = ops.get_all_data()
        for x in response:
            del x["_id"]
        return responses.response(True, None, response)
    except Exception as e:
        return responses.response(False, str(e),"something went wrong please try again")


@app.get("/specific-user", tags=["helpers"])
async def full_user_data(email):
    user = database.user_collection.find_one({"email": email})
    if not user:
        return responses.response(False, "does not exist", str(email))
    return str(user)

@app.post("/user/register_hack", dependencies=[Depends(JWTBearer())],tags=["hack"])
async def register_for_hack(registeration_deets: models.RegisterForHack):
    infoDict = jsonable_encoder(registeration_deets)
    json_hack_deets = dict(infoDict)
    email = infoDict['email']
    hack_name = infoDict["hack_name"]
    print(hack_name)
    if ops.hack_verifier:
        if ops.email_finder(email):
            full_profile = await ops.full_user_data(email)
            user_hacks_resgistered = full_profile["hacks_enlisted"]
            # original_attributes = copy.deepcopy(full_profile["creator_attributes_jobs"])
            user_hacks_resgistered.append(json_hack_deets)
            ops.user_hack_enlisted_updater(infoDict["email"],user_hacks_resgistered )
            return responses.response(True, "hack enlisted!", infoDict)
        else:
            return responses.response(False, "email does not exist", email)
    else:
        return responses.response(False,"hackathon does not exist", hack_name)

@app.post("/submission/")
async def submission(file: UploadFile = File(...), text_field: str = Form(...)):
    file_content = await file.read()  # Read the file's content
    bucket = storage.bucket
    blob = bucket.blob(file.filename)
    blob.upload_from_string(file_content)
    blob.make_public()
    text_dict = json.loads(text_field)
    email = text_dict["email"]
    summary = text_dict["summary"]
    hack_name = text_dict['hack_name']
    timern = datetime.now()
    if ops.hack_verifier:
    
        url = blob.public_url
        full_profile = await ops.full_user_data(email)
        user_submissions  = full_profile["submissions"]


        url_dict = {"_id":0,"submission link": url, "date and time": timern,"summary": summary,"which_hack": hack_name}
        user_submissions.append(url_dict)


        #update user submissions

        ops.user_submissions_updater(text_dict["email"], user_submissions)

        #put it in submission collection
        ops.submission_inserter(url_dict)
        return responses.response(True, "succesfully submitted", url_dict)
    else:
        return responses.response(False,"hackathon does not exist", hack_name)
