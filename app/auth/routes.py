from datetime import timedelta
from typing import Tuple

from flask import Response, request, jsonify
from app import db, jwt
from app.auth import bp
from app.encryption import decrypt_data
from app.models import Users, RevokedTokenModel
from app.schemas import UsersDeserializingSchema
from app.errors.handlers import bad_request, error_response
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
    get_jwt, get_jwt_header,
)
from marshmallow import ValidationError

user_schema = UsersDeserializingSchema()

# Checks if the JWT is on the blacklisted token list
@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_data) -> bool:
    """
    Helper function for checking if a token is present in the database
    revoked token table

    Parameters
    ----------
    jwt_header : dictionary
        header data of the JWT
    jwt_data : dictionary
        payload data of the JWT

    Returns
    -------
    bool
        Returns True if the token is revoked, False otherwise
    """
    jti = jwt_data["jti"]
    return RevokedTokenModel.is_jti_blacklisted(jti)

@bp.post("/register")
def register() -> tuple[Response, int] | Response:
    """
    Endpoint for adding a new user to the database

    Returns
    -------
    str
        A JSON object containing the success message
    """
    try:
        result = user_schema.load(request.get_json())
    except ValidationError as e:
        return bad_request(e.messages)

    if Users.query.filter_by(email=result["email"]).first():
        return bad_request("Email already in use")

    user: Users = Users(
        first_name=result["first_name"],
        last_name=result["last_name"],
        email=result["email"],
        enabled=result["enabled"],
        role=result["role"],
        verified=result["verified"],
    )
    user.set_password(result["password"])

    db.session.add(user)
    db.session.commit()

    # Retrieve user ID after committing to the database
    user_id = user.id

    # Create tokens
    access_token = create_access_token(identity=user_id, fresh=True)
    refresh_token = create_refresh_token(identity=user_id)

    return jsonify({
        "msg": "Successfully registered",
        "user": user_schema.dump(user),
        "token": access_token,
    }), 201

@bp.post("/login")
def login() -> tuple[Response, int] | Response:
    """
    Endpoint for authorizing a user and retrieving a JWT

    Returns
    -------
    str
        A JSON object containing both the access JWT and the refresh JWT
    """
    try:
        result = user_schema.load(request.get_json())
    except ValidationError as e:
        return bad_request(e.messages)

    user = Users.query.filter_by(email=result["email"]).first()

    if user is None or not user.check_password(result["password"]):
        return error_response(401, message="Invalid username or password")

    # Decrypt sensitive keys before returning them
    decrypted_metamask_key = decrypt_data(user.metamask_wallet_address)
    decrypted_coinbase_key = decrypt_data(user.coinbase_wallet_address)
    decrypted_openai_key = decrypt_data(user.openai_api_key)

    tokens = {
        "user": {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "metamask_wallet_address": decrypted_metamask_key,
            "coinbase_wallet_address": decrypted_coinbase_key,
            "openai_api_key": decrypted_openai_key,
            "enabled": user.enabled,
            "role": user.role
        },
        "token": create_access_token(identity=user.id, fresh=True, expires_delta=timedelta(minutes=120)),
    }

    '''
    Add Enable and Role and Id as uuid
    '''

    return jsonify(tokens), 200

@bp.post("/refresh")
@jwt_required(refresh=True)
def refresh() -> tuple[Response, int]:
    """
    Endpoint to retrieve a new access JWT using the refresh JWT.
    A non-fresh access token is returned because the password is not involved in this transaction

    Returns
    -------
    str
        A JSON object containing the new access token
    """
    user_id = get_jwt_identity()
    new_token = create_access_token(identity=user_id, fresh=False)
    payload = {"access_token": new_token}

    return jsonify(payload), 200


@bp.get("/verify")
@jwt_required()
def verify_token() -> tuple[Response, int]:
    """
    Endpoint to verify the current access token

    Returns
    -------
    Response
        A JSON object containing a success message if the token is valid
    """
    try:
        # Get the JWT payload and header
        jwt_payload = get_jwt()
        jwt_header = get_jwt_header()

        # Optionally, you can add more checks here if needed, such as checking if the user still exists in the database
        user_id = get_jwt_identity()

        # Check if the token is revoked
        jti = jwt_payload.get("jti")
        if RevokedTokenModel.is_jti_blacklisted(jti):
            return jsonify({"msg": "Token has been revoked"}), 401

        return jsonify({"msg": "Token is valid", "user_id": user_id}), 200

    except Exception as e:
        return jsonify({"msg": "Token is invalid", "error": str(e)}), 401


@bp.post("/fresh-login")
def fresh_login() -> tuple[Response, int] | Response:
    """
    Endpoint for requesting a new fresh access token

    Returns
    -------
    str
        A JSON object containing
    """
    try:
        result = user_schema.load(request.get_json())
    except ValidationError as e:
        return bad_request(e.messages)

    user = Users.query.filter_by(username=result["username"]).first()

    if user is None or not user.check_password(result["password"]):
        return error_response(401, message="Invalid username or password")

    new_token = create_access_token(identity=user.id, fresh=True)
    payload = {"access_token": new_token}

    return jsonify(payload), 200

@bp.delete("/logout/token")
@jwt_required()
def logout_access_token() -> tuple[Response, int]:
    """
    Endpoint for revoking the current user"s access token

    Returns
    -------
    str
        A JSON object containing the sucess message
    """
    jti = get_jwt()["jti"]
    revoked_token = RevokedTokenModel(jti=jti)
    revoked_token.add()

    return jsonify({"msg": "Successfully logged out"}), 200

@bp.delete("/logout/fresh")
@jwt_required(refresh=True)
def logout_refresh_token() -> tuple[Response, int]:
    """
    Endpoint for revoking the current user"s refresh token

    Returns
    -------
    str
        A JSON object containing a success message
    """
    jti = get_jwt()["jti"]
    revoked_token = RevokedTokenModel(jti=jti)
    revoked_token.add()

    return jsonify({"msg": "Successfully logged out"}), 200
