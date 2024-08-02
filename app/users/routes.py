from flask import request, Response, jsonify
from flask_jwt_extended import current_user, jwt_required, create_access_token
from werkzeug.exceptions import BadRequest

from app.encryption import encrypt_data
from app.errors.handlers import bad_request
from app.models import Users
from app.schemas import UsersSchema
from app.users import bp
from app import db

# Declare database schemas so they can be returned as JSON objects
user_schema = UsersSchema(exclude=("password_hash",))
users_schema = UsersSchema(many=True, exclude=("email", "password_hash"))


@bp.get("/get/user/profile")
@jwt_required()
def user_page() -> tuple[Response, int] | str:
    """
    Let's users retrieve their own user information when logged in

    Returns
    -------
    str
        A JSON object containing the user profile information
    """
    return user_schema.jsonify(current_user), 200


@bp.get("/get/user/profile/<string:username>")
@jwt_required()
def get_user(username: str) -> tuple[Response, int] | Response:
    """
    Lets users retrieve a user profile when logged in

    Parameters
    ----------
    username : str
        The username of the user who's information should be retrieved

    Returns
    -------
    str
        A JSON object containing the user profile information
    """
    user = Users.query.filter_by(username=username).first()

    if user is None:
        return bad_request("User not found")

    return user_schema.jsonify(user), 200


@bp.put("/user")
@jwt_required()
def update_user_profile() -> tuple[Response, int] | Response:
    """
    Lets users update a user profile when logged in

    Returns
    -------
    Response
        A JSON object containing the updated user profile information
    """
    try:
        # Assuming JSON payload
        data = request.get_json()

        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")
        metamask_key = data.get("metamask_wallet_address") or None
        coinbase_key = data.get("coinbase_wallet_address") or None
        openai_key = data.get("openai_api_key") or None

        if not email:
            return bad_request("User Email is required")

    except BadRequest:
        return bad_request("Invalid request data")

    # get the user by id
    user = Users.query.filter_by(email=email).first()

    if user is None:
        return bad_request("User not found")

    # Update fields only if they are provided
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    if email:
        user.email = email
    if metamask_key:
        user.metamask_wallet_address = encrypt_data(metamask_key)
    if coinbase_key:
        user.coinbase_wallet_address = encrypt_data(coinbase_key)
    if openai_key:
        user.openai_api_key = encrypt_data(openai_key)

    # Commit changes to the database
    db.session.commit()

    access_token = create_access_token(identity=user.id, fresh=True)

    return jsonify({
        "user": user_schema.dump(user),
        "token": access_token,
    }), 200
