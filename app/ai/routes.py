from typing import Tuple, Union, Generator
from flask import Response, request, jsonify, stream_with_context
from marshmallow import Schema, fields, ValidationError
from app.ai import bp
from app.errors.handlers import error_response, bad_request
import logging
import json
from solcx import compile_source, install_solc

from app.gen_smart_contract.common import documentation_gen_chain
from app.gen_smart_contract.update_workflow import update_smart_contract_workflow
from app.gen_smart_contract.workflow import smart_contract_generator

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SmartContractSchema(Schema):
    description = fields.Str(required=True)


class UpdateSmartContractSchema(Schema):
    description = fields.Str(required=True)
    contract = fields.Str(required=True)


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
                        {
                            "prompt": smart_contract_description,
                            "error_message": "",
                            "error": "no",
                            "iterations": 0
                         }):
                    for key, value in output.items():
                        logger.info(f"{key}")
                        try:
                            # Convert the Pydantic model instance to a dictionary before serialization
                            if hasattr(value, 'dict'):
                                value = value.dict()
                            json_data = json.dumps({key: value})
                            logger.info(json_data)
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


@bp.post("/smart-contract/update")
def update_smart_contract() -> Union[Tuple[Response, int], Response]:
    """
    Endpoint for updating a smart contract based on the input data.

    Returns
    -------
    Union[Tuple[Response, int], Response]
        The response containing smart contract details or an error message.
    """
    schema = UpdateSmartContractSchema()
    logger.info("Updating smart contract...")
    try:
        data = request.get_json()
        if not data:
            return error_response(400, "No data provided")

        validated_data = schema.load(data)
        smart_contract_description = validated_data["description"]
        smart_contract_code = validated_data["contract"]

        def generate() -> Generator[str, None, None]:
            try:
                for output in update_smart_contract_workflow.stream(
                        {
                            "prompt": smart_contract_description,
                            "existing_contract": smart_contract_code,
                            "error_message": "",
                            "iterations": 0
                        }):
                    for key, value in output.items():
                        logger.info(f"{key}")
                        try:
                            # Convert the Pydantic model instance to a dictionary before serialization
                            if hasattr(value, 'dict'):
                                value = value.dict()
                            json_data = json.dumps({key: value})
                            yield f"{json_data}\n"
                            logger.info(f"{json_data}")
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


@bp.post("/smart-contract/compile")
def compile_solidity():
    try:
        source_code = request.json.get('sourceCode')
        solc_version = request.json.get('solcVersion', '0.8.0')

        if not source_code:
            return jsonify({'success': False, 'errors': ['No source code provided']}), 400

        # Install the requested Solidity compiler version
        install_solc(solc_version)

        compiled_sol = compile_source(
            source_code,
            output_values=['abi', 'bin'],
            solc_version=solc_version
        )

        contract_id, contract_interface = compiled_sol.popitem()
        abi = contract_interface['abi']
        bytecode = contract_interface['bin']

        return jsonify({'success': True, 'abi': abi, 'bytecode': bytecode}), 200

    except Exception as e:
        logger.error(f"Error compiling solidity: {e}")
        return jsonify({'success': False, 'errors': [str(e)]}), 500


@bp.post("/smart-contract/documentation")
def generate_documentation() -> Union[Tuple[Response, int], Response]:
    try:
        source_code = request.json.get('sourceCode')

        if not source_code:
            return jsonify({'success': False, 'errors': ['No source code provided']}), 400

        documentation = documentation_gen_chain.invoke({
            "contract": source_code
        })

        return jsonify({'success': True, 'documentation': documentation.documentation}), 200

    except Exception as e:
        logger.error(f"Error generating documentation: {e}")
        return jsonify({'success': False, 'errors': [str(e)]}), 500
