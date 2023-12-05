import os
import re
from base64 import b64decode, b64encode
from dotenv import load_dotenv
import jsonpickle

from .models import UserID

load_dotenv()

def decode_pickle(obj):
    try:
        user_obj = jsonpickle.decode(b64decode(obj))
            #remove \n
        user_obj = str(user_obj, 'utf-8')
        return user_obj
    except Exception as e:
        print(str(e))
        return "Invalid Command"


def create_flag(user_id):
    os.system("echo " + os.getenv('FLAG') + " > /tmp/" + str(user_id) + ".txt")


def create_pickle(user_id):
    user_obj = UserID(user_id=user_id)
    user_obj = jsonpickle.dumps(user_obj)
    b64 = b64encode(user_obj.encode('utf-8')).decode('utf-8')
    return b64
