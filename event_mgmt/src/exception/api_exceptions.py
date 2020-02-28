import traceback

from flask import Blueprint
from marshmallow.exceptions import ValidationError

from resources import create_response_object

errors = Blueprint('errors', __name__)


class ApiException(Exception):

    def __init__(self, code=None, message=None):
        self.__code__ = code
        self.__message__ = message

    def get_code(self):
        return self.__code__

    def get_message(self):
        return self.__message__


class ValidationException(ApiException):

    def __init__(self, message=[]):
        super().__init__(400, message)


class AuthorizationException(ApiException):

    def __init__(self, message):
        super().__init__(401, message)


class ResourceNotFoundException(ApiException):

    def __init__(self, message):
        super().__init__(404, message)

    def __call__(self, *args, **kwargs):
        return ResourceNotFoundException(self.get_message())


class ErrorResponse():

    def __init__(self, message=[], type=None):
        self.error = message
        self.type = type


@errors.app_errorhandler(ValidationException)
def handle_custom_validation_error(e):
    return create_response_object(ErrorResponse(e.get_message(), 'ValidationError'), 400)


@errors.app_errorhandler(ResourceNotFoundException)
def handle_custom_not_found_error(e):
    return create_response_object(ErrorResponse(e.get_message(), 'NotFound'), 404)


@errors.app_errorhandler(AuthorizationException)
def handle_custom_auth_error(e):
    return create_response_object(ErrorResponse([e.get_message()], 'Auth'), 401)


@errors.app_errorhandler(ValidationError)
def handle_validation_error(e):
    print("\n type is " + str(e.__class__))
    error_dict = e.messages
    errors = []
    for key in error_dict:
        error_message = ','.join(error_dict[key])
        errors.append(f"{key}: {error_message}")

    error_dto = ErrorResponse(errors, 'ValidationError')
    return create_response_object(error_dto, 400)


@errors.app_errorhandler(Exception)
def handle_internal_error(e):
    print(f"\n The error is {e} ")
    traceback.print_exc()
    error_dto = ErrorResponse([str(e)], 'InternalError')
    return create_response_object(error_dto, 500)
