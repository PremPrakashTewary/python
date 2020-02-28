from datetime import datetime, timezone, timedelta

from flask_restful_swagger import swagger
from marshmallow import Schema, fields, validate


class BaseDto:

    def __init__(self, key=None, created_date=None, updated_date=None):
        self.id = key
        self.createdDate = created_date
        self.updatedDate = updated_date

    def to_json(self):
        return self.__dict__

    @staticmethod
    def remove_none(dict_ip):
        out_dict = dict_ip.copy()
        for key, value in dict_ip.items():
            if value is None:
                del out_dict[key]
        return out_dict


class UserDto(BaseDto):

    def __init__(self, key=None, email=None, tenant_id=None, created_date=None, updated_date=None):
        super().__init__(key, created_date, updated_date)
        self.email = email
        self.tenantId = tenant_id

    def to_json(self):
        user_dict = self.__dict__
        return BaseDto.remove_none(user_dict)

    @staticmethod
    def to_obj(key, user_dict):
        return UserDto(key, user_dict['email'], user_dict['tenantId'], user_dict.get('createdDate', None),
                       user_dict.get('updatedDate', None))


class RegisterUserInputSchema(Schema):
    email = fields.Str(required=True, validate=[validate.Email(), validate.Length(min=8)])
    password = fields.Str(required=True, validate=[validate.Length(min=6)])
    tenantId = fields.Str(required=True, validate=[validate.Length(min=4, max=16)])


@swagger.model
class TenantDto(BaseDto):

    def __init__(self, key=None, tenant_id=None, description=None, name=None, created_date=None, updated_date=None):
        super().__init__(key, created_date, updated_date)
        self.tenantId = tenant_id
        self.description = description
        self.name = name

    def to_json(self):
        tenant_dict = self.__dict__
        return BaseDto.remove_none(tenant_dict)

    @staticmethod
    def to_obj(key, tenant_dict):
        return TenantDto(key, tenant_dict['tenantId'], tenant_dict['name'], tenant_dict['description'],
                         tenant_dict['createdDate'], tenant_dict['updatedDate'])


class TenantSchema(Schema):
    tenantId = fields.Str(required=True, validate=[validate.Length(min=4, max=16)])
    name = fields.Str(required=True)
    description = fields.Str()


class JwtPayload(BaseDto):

    def __init__(self, key=None, user_dto=None, status=None):
        super().__init__(key, None, None)
        self.user = user_dto
        self.user.createdDate = None
        self.user.updatedDate = None
        self.exp = datetime.now(timezone.utc) + timedelta(seconds=1)
        self.status = status

    def to_json(self):
        self.user = self.user.to_json()
        jwt_dict = self.__dict__
        return BaseDto.remove_none(jwt_dict)

    @staticmethod
    def to_obj(jwt_dict):
        user_dto = UserDto.to_obj(jwt_dict['user']['id'], jwt_dict['user'])
        jwt = JwtPayload(jwt_dict['id'], user_dto, jwt_dict['status'])
        jwt.exp = jwt_dict.get('exp', None)
        return jwt
