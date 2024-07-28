from typing import Tuple, Union, Generator, Dict, Any
from flask import Response, request, jsonify, stream_with_context
from marshmallow import Schema, fields, ValidationError
from app.ai import bp
from app.errors.handlers import error_response, bad_request
import logging
import json
from app.gen_smart_contract.workflow import smart_contract_generator

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
    logger.info("Generating smart contract...")
    try:
        data = request.get_json()
        if not data:
            return error_response(400, "No data provided")

        validated_data = schema.load(data)
        smart_contract_description = validated_data["description"]

        def generate() -> Generator[str, None, None]:
            try:
                for output in smart_contract_generator.stream(
                        {"messages": [("user", smart_contract_description)], "iterations": 0}):
                    for key, value in output.items():
                        logger.info(f"{key}")
                        try:
                            # Convert the Pydantic model instance to a dictionary before serialization
                            if hasattr(value, 'dict'):
                                value = value.dict()
                            json_data = json.dumps({key: value})
                            yield f"{json_data}\n"
                        except TypeError as e:
                            logger.error(f"Serialization error: {e}")
                            yield json.dumps({"error": f"Serialization error: {e}"})
            except Exception as e:
                logger.error(f"Error generating smart contract: {e}")
                yield json.dumps({"error": f"Error generating smart contract: {e}"})

        return Response(stream_with_context(generate()), mimetype="application/json")

    except ValidationError as err:
        logger.error(f"Validation error: {err.messages}")
        return bad_request(err.messages)

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return error_response(500, "An unexpected error occurred")

# Smart contract workflow definition