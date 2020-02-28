import json

import firebase_admin
from firebase_admin import credentials
from flask import Flask
from flask.json import JSONEncoder
from flask_restful import Api

from api_exceptions import errors
from controller import RegisterationController, PingUserController, LoginController, TenantsController, TenantController
from resources import register, user_ping, tenant_blueprint
from user_dto import BaseDto
from util import EnvSetting

app = Flask(__name__)
app.config.SWAGGER_SUPPORTED_SUBMIT_METHODS = []
api = Api(app)


class CustomJsonEncoder(JSONEncoder):

    def default(self, o):
        if isinstance(o, BaseDto):
            return o.to_json()
        return super(CustomJsonEncoder, o).default(o)


if __name__ == '__main__':
    data = credentials.Certificate(EnvSetting.GOOGLE_CRED_PATH)
    firebase_config = {}
    with open(EnvSetting.FIREBASE_DET) as json_file:
        firebase_config = json.load(json_file)

    default_app = firebase_admin.initialize_app(data)
    app.register_blueprint(register)
    app.register_blueprint(user_ping)
    app.register_blueprint(tenant_blueprint)
    app.register_blueprint(errors)
    app.json_encoder = CustomJsonEncoder
    app.config['JSON_ADD_STATUS'] = True

    api.add_resource(RegisterationController, '/v1/users/register')
    api.add_resource(PingUserController, '/v1/health')
    api.add_resource(TenantsController, '/v1/users/tenants')
    api.add_resource(LoginController, '/v1/users/login')
    api.add_resource(TenantController, '/v1/users/tenants/<string:id>')
    app.run(debug=True)
