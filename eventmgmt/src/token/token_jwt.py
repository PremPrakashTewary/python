import uuid
from datetime import datetime, timezone, timedelta
from functools import wraps

import jwt
from flask import request, after_this_request
from jwt import ExpiredSignatureError

from api_exceptions import AuthorizationException
from user_dto import JwtPayload
from util import EnvSetting


def token_required(f):
    @wraps(f)
    def verify_auth_token(*args, **kwargs):
        token = request.headers.get('Authorization', None)
        token_sub = True
        if not token:
            token = request.cookies.get('Bearer', None)
            token_sub = False
        if not token:
            raise AuthorizationException('Missing token')
        if token_sub:
            token = token[len('Bearer '):]
        try:
            data_jwt = jwt.decode(token, key=EnvSetting.SECRET_KEY, algorithms='HS256')
            data_jwt = JwtPayload.to_obj(data_jwt)
        except ExpiredSignatureError as exp:
            print(f"\n The error is {exp} refresh token now")
            __refresh_jwt__()
        except Exception as exp:
            print(f"\n The error is {exp}")
            raise AuthorizationException('Invalid token')
        return f(*args, **kwargs)

    return verify_auth_token


def create_jwt_token(user_info=None, is_fresh=False, is_refresh=False):
    fresh_status = 'unfresh'
    if is_fresh:
        fresh_status = 'fresh'
    if is_refresh:
        jwt_payload = JwtPayload(str(uuid.uuid4()), user_info, 'refresh_token')
        jwt_payload.exp = None
    else:
        jwt_payload = JwtPayload(str(uuid.uuid4()), user_info, fresh_status)
    return __jwt_encode__(jwt_payload)


def __jwt_encode__(jwt_payload):
    jwt_token = jwt.encode(jwt_payload.to_json(), key=EnvSetting.SECRET_KEY, algorithm='HS256')
    jwt_token = str(jwt_token, 'utf-8')
    return jwt_token


def __refresh_jwt__():
    refresh_token = request.cookies.get('refresh_token', None)
    if not refresh_token:
        raise AuthorizationException('Token expired use refresh token')
    refresh_token = jwt.decode(refresh_token, key=EnvSetting.SECRET_KEY, algorithms='HS256')
    refresh_token = JwtPayload.to_obj(refresh_token)
    refresh_token.status = 'unfresh'
    refresh_token.exp = datetime.now(timezone.utc) + timedelta(minutes=10)
    new_jwt_token = __jwt_encode__(refresh_token)

    @after_this_request
    def after_request(response):
        response.set_cookie('Bearer', new_jwt_token)
        return response
