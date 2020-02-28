import string

from api_exceptions import ValidationException
from register_dao import UserRepository, TenantRepository
from user_dto import RegisterUserInputSchema, TenantSchema, TenantDto
from util import encrypt_text


class RegisterationService:

    def __init__(self):
        self.__reg_repo = UserRepository()
        self.__schema = RegisterUserInputSchema()
        self.__tenant_repo = TenantRepository()

    def register_user(self, user_data):
        self.__schema.load(user_data)
        users = self.__reg_repo.get_user_by_email(user_data['email'])
        error_msgs = []
        if len(users) > 0:
            error_msgs.append("'email': user already exists for the email")
        tenants = self.__tenant_repo.get_tenant_by_tenant_id(user_data['tenantId'])
        if len(tenants) == 0:
            error_msgs.append("'tenantId': tenant not found")

        if len(error_msgs) > 0:
            raise ValidationException(error_msgs)

        user_data['password'] = encrypt_text(user_data['password'])
        self.__tenant_repo.get_tenant_by_tenant_id(user_data['tenantId'])
        return self.__reg_repo.insert(user_data)


class TenantService:

    def __init__(self):
        self.__tenant_repo = TenantRepository()
        self.__schema = TenantSchema()

    def create_tenant(self, tenant_data):
        self.__schema.load(tenant_data)
        tenants = self.__tenant_repo.get_tenant_by_tenant_id(tenant_data['tenantId'])
        if len(tenants):
            raise ValidationException(['Tenant already exists for the given tenantId'])
        return self.__tenant_repo.insert(tenant_data)

    def get_all(self):
        tenants = self.__tenant_repo.get_all()
        tenant_dto = []
        for key in tenants:
            tenant_dto.append(TenantDto.to_obj(key, tenants[key]))
        return tenant_dto

    def get_by_id(self, id_or_key:string):
        return self.__tenant_repo.get_by_id(id_or_key)
