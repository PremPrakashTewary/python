from flask import request
from flask_restful import Resource
from flask_restful_swagger import swagger

from api_exceptions import ResourceNotFoundException
from register_service import RegisterationService, TenantService
from resources import create_response_object, create_response
from response_dto import CreateResponseDto, HealthResponse
from service import UserService
from token_jwt import create_jwt_token, token_required


class RegisterationController(Resource):

    def __init__(self):
        self.__service__ = RegisterationService()

    @swagger.operation(
        notes='API to register user',
        responseClass=CreateResponseDto.__name__,
        parameters=[
            {
                "email": "email@email.com",
                "password": "password"
            }
        ]
    )
    def post(self):
        user_id = self.__service__.register_user(request.json)
        return create_response_object(CreateResponseDto(user_id), 201)


class PingUserController(Resource):

    def __init__(self):
        pass

    def get(self):
        return create_response_object(HealthResponse('UP'), 200)


class TenantsController(Resource):

    def __init__(self):
        self.__tenant_service__ = TenantService()

    @token_required
    def post(self):
        id = self.__tenant_service__.create_tenant(request.json)
        return create_response_object(CreateResponseDto(id), 201)

    @token_required
    def get(self):
        return create_response(self.__tenant_service__.get_all(), 200)


class TenantController(Resource):

    def __init__(self):
        self.__tenant_service__ = TenantService()

    @token_required
    def get(self, id):
        tenant_dict = self.__tenant_service__.get_by_id(id).get_or_raise(exception=
                                                                         ResourceNotFoundException(
                                                                             'Tenant not found for given id'))
        return create_response(tenant_dict, 200)


class LoginController(Resource):

    def __init__(self):
        self.__user_service__ = UserService()

    def post(self):
        user_data = request.json
        user_got = self.__user_service__.validate_user(user_data)
        jwt_token = create_jwt_token(user_got, True)
        refresh_token = create_jwt_token(user_got, False, True)
        response = create_response({'status': 'success'}, 200)
        response.set_cookie('Bearer', jwt_token)
        response.set_cookie('refresh_token', refresh_token)
        return response
