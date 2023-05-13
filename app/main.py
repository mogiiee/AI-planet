from fastapi import FastAPI, HTTPException, Depends, File, UploadFile, Form
from fastapi.encoders import jsonable_encoder
from . import responses, database, ops, models, exporter
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

firebase_admin.initialize_app(cred, {"storageBucket": "gs://ai-planet.appspot.com"})

# index page
@app.get("/")
async def greet():
    return {"hello": "people from AI planet"}


# gets all the hacks created
@app.get("/GetAllHacks", tags=["helpers"])
async def Get_all_hacks():
    metadata = ops.get_all_hacks()
    for x in metadata:
        del x["_id"]
    return responses.response(True, None, metadata)


# login using jwt tokens for safety
@app.post("/login", tags=["auth"])
async def login(login_details: models.UserLoginSchema):
    infoDict = jsonable_encoder(login_details)
    print(infoDict)
    email = infoDict["email"]
    password = infoDict["password"]
    # Verify credentials
    if await ops.verify_credentials(email, password):
        return responses.response(True, "logged in", signJWT(infoDict))
    else:
        raise HTTPException(401, "unauthorised login or email is wrong")


# new user sign up
@app.post("/signup", tags=["auth"])
async def signup(signup_details: models.User):
    infoDict = jsonable_encoder(signup_details)
    # print(infoDict)
    infoDict = dict(infoDict)
    # Checking if email already exists
    email_count = database.user_collection.count_documents({"email": infoDict["email"]})
    if email_count > 0:
        return responses.response(False, "duplicated user, email already in use", None)
    # Insert new user

    encoded_password = ops.hash_password(str(infoDict["password"]))
    infoDict["password"] = encoded_password
    # print(infoDict)
    json_signup_details = jsonable_encoder(infoDict)
    await ops.inserter(json_signup_details)
    return responses.response(True, "inserted", signJWT(infoDict))


# protected routes of adding a new hack
schema = {
    "title": "hi hack",
    "description": "string",
    "email": "user@example.com",
    "background_image": "string",
    "hackathon_image": "string",
    "submission_type": "link",
    "start_datetime": "2023-05-13T05:25:18.995Z",
    "end_datetime": "2023-05-13T05:25:18.995Z",
    "reward_prize": 0,
}


@app.post(
    "/user/add_hack", dependencies=[Depends(JWTBearer())], tags=["hack", "protected"],
)
async def add_hack(
    text_field: str = Form(...),
    hackathon_image: UploadFile = File(...),
    background_image: UploadFile = File(...),
):
    text_dict = json.loads(text_field)
    email = text_dict["email"]
    hack_name = text_dict["title"]
    file_content1 = await hackathon_image.read()  # Read the file's content
    file_content2 = await background_image.read()  # Read the file's content
    bucket = storage.bucket
    blob_hack_img = bucket.blob(hackathon_image.filename)
    blob_hack_img.upload_from_string(file_content1)
    blob_hack_img.make_public()
    blob_background_image = bucket.blob(background_image.filename)
    blob_background_image.upload_from_string(file_content2)
    blob_background_image.make_public()
    if ops.hack_verifier(hack_name):
        print("ihkuhdfisjdfsdfdsf")
        if ops.email_finder(email):
            full_profile = await ops.full_user_data(email)

            user_hacks_created = full_profile["hacks_created"]
            url_hack_img = blob_hack_img.public_url
            url_background_image = blob_background_image.public_url
            text_dict["hackathon_image"] = url_hack_img
            text_dict["background_image"] = url_background_image
            user_hacks_created.append(text_dict)
            ops.user_hack_created_updater(text_dict["email"], user_hacks_created)
            ops.hack_inserter(text_dict)

            return responses.response(True, "hack posted!", str(text_dict))
        else:
            return responses.response(False, "email does not exist", email)
    else:
        return responses.response(
            False, "hackathon already exists try a different title", hack_name
        )


#  { "hack_name": "hi hack",   "summary": "string",   "email": "q@q.com",   "type_of_submission": "file",   "hackathon_image": "string",   "submission_type": "link",   "start_datetime": "2023-05-13T05:25:18.995Z",   "end_datetime": "2023-05-13T05:25:18.995Z",   "reward_prize": 0 }

# https://nscsso.my.site.com/student/s/article/Why-am-I-getting-the-error-message-Failed-to-Load-PDF-document-when-I-try-to-view-my-ePDF-transcript#:~:text=The%20%E2%80%9CFailed%20to%20Load%20PDF,opened%20with%20Adobe%20Acrobat%20Reader.


@app.post("/submission/", tags=["hack"])
async def submission(file: UploadFile = File(...), text_field: str = Form(...)):
    file_content = await file.read()  # Read the file's content
    bucket = storage.bucket
    blob = bucket.blob(file.filename)
    blob.upload_from_string(file_content)
    blob.make_public()
    text_dict = json.loads(text_field)
    email = text_dict["email"]
    summary = text_dict["summary"]
    hack_name = text_dict["hack_name"]
    type_of_submission = text_dict["type_of_submission"]
    timern = datetime.now()
    print(hack_name)
    if not ops.hack_verifier(hack_name):

        url = blob.public_url
        full_profile = await ops.full_user_data(email)
        user_submissions = full_profile["submissions"]
        all_hacks = Get_all_hacks()
        print(all_hacks)

        url_dict = {
            "submission link": url,
            "date and time": timern,
            "summary": summary,
            "which_hack": hack_name,
            "type of submission": type_of_submission,
        }

        user_submissions.append(url_dict)

        # update user submissions

        ops.user_submissions_updater(text_dict["email"], user_submissions)

        # put it in submission collection
        ops.submission_inserter(url_dict)
        return responses.response(True, "succesfully submitted", str(url_dict))
    else:
        return responses.response(False, "hackathon does not exist", hack_name)


# protected routes of registering for a new hack


@app.post(
    "/user/register_hack",
    dependencies=[Depends(JWTBearer())],
    tags=["hack", "protected"],
)
async def register_for_hack(registeration_deets: models.RegisterForHack):
    infoDict = jsonable_encoder(registeration_deets)
    json_hack_deets = dict(infoDict)
    email = infoDict["email"]
    hack_name = infoDict["hack_name"]
    print(hack_name)
    if ops.hack_verifier:
        if ops.email_finder(email):
            full_profile = await ops.full_user_data(email)
            user_hacks_resgistered = full_profile["hacks_enlisted"]
            # original_attributes = copy.deepcopy(full_profile["creator_attributes_jobs"])
            user_hacks_resgistered.append(json_hack_deets)
            ops.user_hack_enlisted_updater(infoDict["email"], user_hacks_resgistered)
            return responses.response(True, "hack enlisted!", infoDict)
        else:
            return responses.response(False, "email does not exist", email)
    else:
        return responses.response(False, "hackathon does not exist", hack_name)


@app.get("/all-users", tags=["helpers"])
async def Get_all_data():
    try:
        response = ops.get_all_data()
        for x in response:
            del x["_id"]
        return responses.response(True, None, response)
    except Exception as e:
        return responses.response(
            False, str(e), "something went wrong please try again"
        )


@app.get("/specific-user", tags=["helpers"])
async def full_user_data(email):
    user = database.user_collection.find_one({"email": email})
    if not user:
        return responses.response(False, "does not exist", str(email))
    return str(user)
