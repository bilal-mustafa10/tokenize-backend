from app import ma
from app.models import Users

from marshmallow import Schema, fields


class UsersSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Users


class UsersDeserializingSchema(Schema):
    password = fields.String()
    first_name = fields.String()
    last_name = fields.String()
    email = fields.Email()
    enabled = fields.Boolean()
    role = fields.String()
    verified = fields.Boolean()
