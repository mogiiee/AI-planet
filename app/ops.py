from . import database
from bson import ObjectId
from . import database, responses
import bcrypt


async def email_finder(email):
    existing_user = database.user_collection.find_one({"email": email})
    if existing_user is not None:
        return False
    else:
        return True


def hash_password(password: str) -> str:
    # Hash the password using bcrypt
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    # Return the hashed password as a string
    return hashed_password.decode("utf-8")


async def verify_credentials(username: str, password: str) -> bool:
    user = await email_finder(username)
    if user is None:
        return False
    hashed_password = user["password"].encode("utf-8")
    is_valid_password = bcrypt.checkpw(password.encode("utf-8"), hashed_password)
    return is_valid_password