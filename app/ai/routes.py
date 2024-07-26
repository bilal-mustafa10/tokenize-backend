from typing import Tuple, Union

from flask import Response, request, jsonify
from marshmallow import Schema, fields, ValidationError

from app.ai import bp
from app.ai.generate_smart_contract import generate_smart_contract_logic
from app.errors.handlers import error_response, bad_request
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SmartContractSchema(Schema):
    description = fields.Str(required=True)


@bp.post("/smart-contract")
def generate_smart_contract() -> Union[Tuple[Response, int], Response]:
    """
    Endpoint for generating a smart contract based on the input data.

    Returns
    -------
    Union[Tuple[Response, int], Response]
        The response containing smart contract details or an error message.
    """
    schema = SmartContractSchema()
    try:
        data = request.get_json()
        if not data:
            return error_response(400, "No data provided")

        validated_data = schema.load(data)
        smart_contract_description = validated_data["description"]

        try:
            smart_contract_details = generate_smart_contract_logic(smart_contract_description)
            return jsonify(smart_contract_details.dict()), 200
        except Exception as e:
            logger.error(f"Error generating smart contract: {e}")
            return error_response(400, f"Error generating smart contract: {e}")

    except ValidationError as err:
        logger.error(f"Validation error: {err.messages}")
        return bad_request(err.messages)

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return error_response(500, "An unexpected error occurred")
