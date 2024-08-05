import logging
from flask import request, jsonify, Response
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import BadRequest

from app import db
from app.models import SmartContract, SmartContractVersion, Users
from app.schemas import SmartContractSchema
from app.smart_contract import bp

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

smart_contract_schema = SmartContractSchema()
smart_contracts_schema = SmartContractSchema(many=True)


def add_smart_contract_version(version_data, smart_contract_id):
    """
    Adds a new version to a smart contract.

    Parameters
    ----------
    version_data : dict
        The data for the new version.
    smart_contract_id : int
        The ID of the smart contract to add the version to.
    """
    try:
        new_version = SmartContractVersion(contract_type=version_data.get("contract_type"),
                                           code_requirements=version_data.get("code_requirements"),
                                           documentation=version_data.get("documentation"),
                                           code=version_data.get("code"), deployed=version_data.get("deployed"),
                                           compiler_version=version_data.get("compiler_version"),
                                           smart_contract_id=smart_contract_id)
        db.session.add(new_version)
    except Exception as e:
        logger.error(f"Error adding smart contract version: {e}")
        raise


def validate_smart_contract_data(data):
    """
    Validates the required fields in the smart contract data.

    Parameters
    ----------
    data : dict
        The data to validate.

    Raises
    ------
    BadRequest
        If any required field is missing.
    """
    required_fields = ["name", "draft", "deployed_id", "wallet_address", "network"]
    for field in required_fields:
        if field not in data:
            raise BadRequest(f"Missing required field: {field}")


@bp.get("/smart_contract")
@jwt_required()
def get_smart_contracts() -> tuple[Response, int]:
    """
    Returns all smart contracts submitted by the user making the request.

    Returns
    -------
    tuple[Response, int]
        A JSON object containing all smart contract data and HTTP status code
    """
    try:
        user_id = get_jwt_identity()
        smart_contracts = SmartContract.query.filter_by(user_id=user_id).all()
        smart_contracts_data = smart_contracts_schema.dump(smart_contracts)

        return jsonify(smart_contracts_data), 200

    except BadRequest as e:
        logger.error(f"Validation error: {e}")
        return jsonify({"error": str(e)}), 400
    except SQLAlchemyError as e:
        logger.error(f"Database error: {e}")
        return jsonify({"error": "Database error"}), 500
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return jsonify({"error": "Internal server error"}), 500


@bp.post("/smart_contract")
@jwt_required()
def add_smart_contract() -> tuple[Response, int] | Response:
    """
    Adds a new smart contract.

    Returns
    -------
    tuple[Response, int] | Response
        A JSON object containing the new smart contract data and HTTP status code
    """
    try:
        data = request.json
        validate_smart_contract_data(data)

        user_id = get_jwt_identity()


        smart_contract = SmartContract(user_id=user_id, name=data["name"], draft=data["draft"],
                                       deployed_id=data["deployed_id"], wallet_address=data["wallet_address"],
                                       network=data["network"])

        db.session.add(smart_contract)
        db.session.commit()

        versions = data.get("versions", [])
        for version in versions:
            add_smart_contract_version(version, smart_contract.id)

        db.session.commit()

        # Fetch the newly created smart contract including its versions
        new_contract = SmartContract.query.filter_by(id=smart_contract.id).first()
        result = smart_contract_schema.dump(new_contract)

        return jsonify(result), 201

    except BadRequest as e:
        logger.error(f"Validation error: {e}")
        return jsonify({"error": str(e)}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Database error: {e}")
        return jsonify({"error": "Database error"}), 500
    except Exception as e:
        db.session.rollback()
        logger.error(f"Unexpected error: {e}")
        return jsonify({"error": "Internal server error"}), 500


@bp.put("/smart_contract/<int:id>")
@jwt_required()
def update_smart_contract(id: int) -> tuple[Response, int] | Response:
    """
    Updates a smart contract by its ID.

    Parameters
    ----------
    id : int
        The ID of the smart contract

    Returns
    -------
    tuple[Response, int] | Response
        A JSON object containing the updated smart contract data and HTTP status code
    """
    try:
        user_id = get_jwt_identity()

        data = request.json

        smart_contract = SmartContract.query.filter_by(id=id).first()
        if not smart_contract:
            return jsonify({"error": "Smart contract not found"}), 404



        logger.info(f"User ID: {user_id}")
        logger.info(f"Smart contract ID: {smart_contract.user_id}")
        if str(smart_contract.user_id) != str(user_id):
            return jsonify({"error": "User does not belong to this smart contract"}), 403

        logger.info(f"Updating smart contract {smart_contract.id}")

        smart_contract.name = data["name"]
        smart_contract.draft = data["draft"]
        smart_contract.deployed_id = data["deployed_id"]
        smart_contract.wallet_address = data["wallet_address"]
        smart_contract.network = data["network"]

        versions = data.get("versions", [])
        for version_data in versions:
            version_id = version_data.get("id")
            if not version_id:
                logger.info("Creating new version")
                add_smart_contract_version(version_data, id)
            else:
                version = SmartContractVersion.query.filter_by(id=version_id, smart_contract_id=id).first()
                if version:
                    logger.info(f"Updating smart contract version {version_id}")
                    version.contract_type = version_data["contract_type"]
                    version.code_requirements = version_data["code_requirements"]
                    version.documentation = version_data["documentation"]
                    version.code = version_data["code"]
                    version.deployed = version_data["deployed"]
                    version.compiler_version = version_data["compiler_version"]

        db.session.commit()

        updated_contract = SmartContract.query.filter_by(id=smart_contract.id).first()
        result = smart_contract_schema.dump(updated_contract)

        return jsonify({"message": "Smart contract updated successfully", "smart_contract": result}), 200

    except BadRequest as e:
        logger.error(f"Validation error: {e}")
        return jsonify({"error": str(e)}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Database error: {e}")
        return jsonify({"error": "Database error"}), 500
    except Exception as e:
        db.session.rollback()
        logger.error(f"Unexpected error: {e}")
        return jsonify({"error": "Internal server error"}), 500


@bp.delete("/smart_contract/<int:id>")
@jwt_required()
def delete_smart_contract(id: int) -> tuple[Response, int] | Response:
    """
    Deletes a smart contract by its ID along with all its versions.

    Parameters
    ----------
    id : int
        The ID of the smart contract

    Returns
    -------
    tuple[Response, int] | Response
        A JSON object containing a success message and HTTP status code
    """
    try:
        user_id = get_jwt_identity()
        smart_contract = SmartContract.query.filter_by(id=id).first()

        if not smart_contract:
            return jsonify({"error": "Smart contract not found"}), 404


        logger.info(f"User ID: {user_id}")
        logger.info(f"Smart contract ID: {smart_contract.user_id}")
        if str(smart_contract.user_id) != str(user_id):
            return jsonify({"error": "You are not authorized to delete this smart contract"}), 401

        # Fetch all versions associated with the smart contract
        versions = SmartContractVersion.query.filter_by(smart_contract_id=id).all()

        # Delete all associated versions
        for version in versions:
            db.session.delete(version)

        # Delete the smart contract
        db.session.delete(smart_contract)
        db.session.commit()

        return jsonify({"message": "Smart contract and its versions deleted successfully"}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Database error: {e}")
        return jsonify({"error": "Database error"}), 500
    except Exception as e:
        db.session.rollback()
        logger.error(f"Unexpected error: {e}")
        return jsonify({"error": "Internal server error"}), 500
