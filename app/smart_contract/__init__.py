from flask import Blueprint

bp = Blueprint("smartcontract", __name__)

from app.smart_contract import routes
