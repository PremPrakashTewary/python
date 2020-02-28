import json

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

from util import EnvSetting

data = credentials.Certificate(EnvSetting.GOOGLE_CRED_PATH)
firebase_config = {}
with open(EnvSetting.FIREBASE_DET) as json_file:
    firebase_config = json.load(json_file)

default_app = firebase_admin.initialize_app(data, {'databaseURL': firebase_config['databaseURL']})
print(default_app.project_id)
ref = db.reference('users')
user_list = ref.order_by_child("email_id").equal_to("premparakashtewary80@gmail.com").get()
if len(user_list) == 0:
    print("\n No data")
elif len(user_list) > 1:
    print("\n multiple data")
else:
    keys = list(user_list.keys())
    key = keys[0]
    print("\n some " + key)
    user_data = user_list[key]
    print("\n user data " + str(user_data))
print("\n key")