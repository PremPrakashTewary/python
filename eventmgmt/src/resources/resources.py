from flask import Blueprint, jsonify

register = Blueprint('register', __name__)
user_ping = Blueprint('users', __name__)
tenant_blueprint = Blueprint('tenants', __name__)


def create_response(dict, status):
    rsp = jsonify(dict)
    rsp.status_code = status
    return rsp


def create_response_object(obj, status):
    return create_response(obj.__dict__, status)