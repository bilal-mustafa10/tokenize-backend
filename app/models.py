from app import db, jwt
import uuid
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


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
    openai_api_key = db.Column(db.Text, default=None, nullable=True)
    metamask_wallet_address = db.Column(db.Text, default=None, nullable=True)
    coinbase_wallet_address = db.Column(db.Text, default=None, nullable=True)
    smart_contracts = db.relationship('SmartContract', backref='user', lazy=True)

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

    def get_smart_contracts(self) -> dict:
        """
        Helper function to retrieve all the smart contracts associated with this user

        Returns
        ----------
        dict
            A dictionary containing all the smart contracts associated with this user
        """
        return SmartContract.query.filter_by(user_id=self.id).all()

    def get_smart_contract(self, smart_contract_id: int) -> dict:
        """
        Helper function to retrieve a smart contract by id

        Parameters
        ----------
        smart_contract_id : int
            The id of the smart contract to retrieve

        Returns
        ----------
        dict
            A dictionary containing the smart contract by its id
        """

        return SmartContract.query.filter_by(id=smart_contract_id, user_id=self.id).first()


class SmartContractVersion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    smart_contract_id = db.Column(db.Integer, db.ForeignKey('smart_contract.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    contract_type = db.Column(db.String(255), nullable=False)
    code_requirements = db.Column(db.Text, nullable=False)
    code = db.Column(db.Text, nullable=False)
    documentation = db.Column(db.Text, nullable=False)
    deployed = db.Column(db.Boolean, default=False, nullable=False)
    compiler_version = db.Column(db.String(255), nullable=False)


class SmartContract(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    draft = db.Column(db.Boolean, nullable=False, default=True)
    deployed_id = db.Column(db.String(255), nullable=True)
    wallet_address = db.Column(db.String(255), nullable=True)
    network = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    versions = db.relationship("SmartContractVersion", backref="smart_contract")


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
