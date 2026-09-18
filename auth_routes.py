from flask import Blueprint
from controllers.auth_controller import register_user, login_user, get_current_user
from middleware.auth_middleware import token_required

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

auth_bp.route('/register', methods=['POST'])(register_user)
auth_bp.route('/login', methods=['POST'])(login_user)
auth_bp.route('/logout', methods=['POST'])(lambda: ({'message': 'Logged out'}, 200))
auth_bp.route('/me', methods=['GET'])(token_required(get_current_user))