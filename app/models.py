from app import db, jwt
import uuid
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


@jwt.user_lookup_loader
def user_loader_callback(jwt_header: dict, jwt_data: dict) -> object:
    """
    HUser loader function which uses the JWT identity to retrieve a user object.
    Method is called on protected routes

    Parameters
    ----------
    jwt_header : dictionary
        header data of the JWT
    jwt_data : dictionary
        payload data of the JWT

    Returns
    -------
    object
        Returns a users object containing the user information
    """
    return Users.query.filter_by(id=jwt_data["sub"]).first()


# defines the Users database table
class Users(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), unique=False, nullable=False)
    enabled = db.Column(db.Boolean, default=True, nullable=False)
    role = db.Column(db.String(50), nullable=False, default='user')
    verified = db.Column(db.Boolean, default=False, nullable=False)

    def set_password(self, password: str):
        """
        Helper function to generate the password hash of a user

        Parameters
        ----------
        password : str
            The password provided by the user when registering
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """
        Helper function to verify the password hash against the password provided
        by the user when logging in

        Parameters
        ----------
        password : str
            The password provided by the user when logging in

        Returns
        -------
        bool
            Returns True if the password is a match. If not, False is returned
        """
        return check_password_hash(self.password_hash, password)


class RevokedTokenModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120))
    date_revoked = db.Column(db.DateTime, default=datetime.utcnow)

    def add(self):
        """
        Helper function to add a JWT to the table
        """
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_jti_blacklisted(cls, jti: str) -> bool:
        """
        Helper function to check if a JWT is in the Revoked Token table

        Parameters
        ----------
        jti : str
            The JWT unique identifier

        Returns
        -------
        bool
            Return True if the JWT is in the Revoked Token table
        """
        query = cls.query.filter_by(jti=jti).first()
        return bool(query)
