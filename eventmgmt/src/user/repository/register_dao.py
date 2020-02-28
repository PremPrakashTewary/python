import string
from datetime import datetime, timezone
from firebase_admin import firestore
from pyOptional import Optional


def convert_doc_to_dict(docs):
    doc_dict = {}
    for doc in docs:
        doc_dict[doc.id] = doc.to_dict()
    return doc_dict


class BaseRepository():

    def __init__(self, path):
        self.ref = firestore.client().collection(path)

    def insert(self, data):
        data['createdDate'] = str(datetime.now(timezone.utc))
        data['updatedDate'] = str(datetime.now(timezone.utc))
        new_data = self.ref.add(data)
        return new_data[1].id

    def get_all(self):
        return convert_doc_to_dict(self.ref.stream())

    def get_by_id(self, id_or_key: string):
        doc_data = self.ref.document(id_or_key)
        doc_data = doc_data.get().to_dict()
        return Optional(doc_data)


class UserRepository(BaseRepository):

    def __init__(self):
        super().__init__("users")

    def get_user_by_email(self, email):
        return convert_doc_to_dict(self.ref.where('email', '==', email).stream())


class TenantRepository(BaseRepository):

    def __init__(self):
        super().__init__("tenants")

    def get_tenant_by_tenant_id(self, tenant_id):
        return convert_doc_to_dict(self.ref.where('tenantId', '==', tenant_id).stream())
