from app import ma
from app.models import Users, SmartContract, SmartContractVersion

from marshmallow import Schema, fields, pre_load


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
    openai_api_key = fields.String()
    metamask_wallet_address = fields.String()
    coinbase_wallet_address = fields.String()


class SmartContractVersionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SmartContractVersion
        include_fk = True
        load_instance = True

    @pre_load
    def exclude_smart_contract_id(self, data, **kwargs):
        if 'smart_contract_id' in data:
            del data['smart_contract_id']
        return data


class SmartContractSchema(ma.SQLAlchemyAutoSchema):
    versions = fields.Nested(SmartContractVersionSchema, many=True)

    class Meta:
        model = SmartContract
        include_relationships = True
        load_instance = True
