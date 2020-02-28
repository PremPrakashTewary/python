import firebase_admin
from firebase_admin import auth
from firebase_admin import credentials

from util import EnvSetting

data = credentials.Certificate(EnvSetting.GOOGLE_CRED_PATH)
default_app = firebase_admin.initialize_app(credential=data)
print(default_app.name)
user_record = auth.create_user(email='premparakashtewary80@gmail.com')
auth.set_custom_user_claims(user_record.uid, {"some": "value"})
#user_record = auth.get_user_by_email('premprakashtewary80@gmail.com')
print("\n got")

token = auth.create_custom_token(user_record.uid, app=default_app)
print("\n got token bytes")
token = token.decode('utf-8')
print("\n str token " + token)