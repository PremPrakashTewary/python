from api_exceptions import AuthorizationException
from register_dao import UserRepository
from user_dto import RegisterUserInputSchema, UserDto
from util import check_text


class UserService:

    def __init__(self):
        self.__user_repo__ = UserRepository()
        self.__user_schema__ = RegisterUserInputSchema()

    def validate_user(self, user_data):
        self.__user_schema__.load(user_data)
        user_dict = self.__user_repo__.get_user_by_email(user_data.get('email'))
        if len(user_dict) != 1:
            raise AuthorizationException(message='Invalid credientails')
        user_got = None
        for user_id in user_dict:
            user_got = UserDto.to_obj(user_id, user_dict[user_id])
            password = user_dict[user_id]['password']
        valid_password = check_text(user_data.get('password'), password)
        if not valid_password:
            raise AuthorizationException(message='Invalid credientails')
        return user_got
