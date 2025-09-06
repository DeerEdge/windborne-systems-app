from flask import Blueprint

api_bp = Blueprint('api', __name__)

# Import all route modules
from app.api import routes
