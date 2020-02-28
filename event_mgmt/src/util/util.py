import os

import bcrypt

from user_dto import TenantDto, UserDto


def encrypt_text(text):
    return bcrypt.hashpw(text, bcrypt.gensalt())


def check_text(text, hashed_text):
    return bcrypt.checkpw(text, hashed_text)


class EnvSetting:
    GOOGLE_CRED_PATH = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS',
                                      '/Users/xbbnpfg/Downloads/user-details-cb36b-6bca941497e4.json')
    FIREBASE_DET = os.environ.get('FIRE_BASE_DET', '/Users/xbbnpfg/Downloads/firebase_api.json')
    SECRET_KEY = os.environ.get('SECRET_KEY', 'authkey')
