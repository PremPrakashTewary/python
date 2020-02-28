from flask_restful_swagger import swagger
from flask_serialize import FlaskSerializeMixin


@swagger.model
class CreateResponseDto(FlaskSerializeMixin):

    def __init__(self, id):
        self.id = id


@swagger.model
class HealthResponse(FlaskSerializeMixin):

    def __init__(self, status):
        self.status = status
