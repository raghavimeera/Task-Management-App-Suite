from flask import Blueprint
from controllers.task_controller import get_tasks, create_task, update_task, delete_task, clear_all_tasks
from middleware.auth_middleware import token_required

task_bp = Blueprint('tasks', __name__, url_prefix='/api/tasks')

@task_bp.route('', methods=['GET'])
@token_required
def fetch_tasks(current_user):
    return get_tasks(current_user)

@task_bp.route('', methods=['POST'])
@token_required
def add_task(current_user):
    return create_task(current_user)

@task_bp.route('/<int:task_id>', methods=['PUT'])
@token_required
def edit_task(current_user, task_id):
    return update_task(current_user, task_id)

@task_bp.route('/<int:task_id>', methods=['DELETE'])
@token_required
def remove_task(current_user, task_id):
    return delete_task(current_user, task_id)

@task_bp.route('', methods=['DELETE'])
@token_required
def purge_tasks(current_user):
    return clear_all_tasks(current_user)