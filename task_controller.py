from flask import request, jsonify
from database import db
from models.task_model import Task
from datetime import datetime

def get_tasks(current_user):
    tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.created_at.desc()).all()
    return jsonify([task.to_dict() for task in tasks]), 200

def create_task(current_user):
    data = request.get_json()
    title = data.get('title')

    if not title or not title.strip():
        return jsonify({'message': 'Task title is required!'}), 400

    due_date = None
    if data.get('due_date'):
        try:
            due_date = datetime.strptime(data.get('due_date'), '%Y-%m-%d').date()
        except ValueError:
            pass

    new_task = Task(
        user_id=current_user.id,
        title=title.strip(),
        description=data.get('description', ''),
        priority=data.get('priority', 'Medium'),
        category=data.get('category', 'General'),
        due_date=due_date
    )

    db.session.add(new_task)
    db.session.commit()

    return jsonify(new_task.to_dict()), 201

def update_task(current_user, task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()

    if not task:
        return jsonify({'message': 'Task not found or access denied!'}), 404

    data = request.get_json()

    if 'title' in data:
        if not data['title'].strip():
            return jsonify({'message': 'Task title cannot be empty!'}), 400
        task.title = data['title'].strip()

    if 'description' in data:
        task.description = data['description']

    if 'priority' in data:
        task.priority = data['priority']

    if 'category' in data:
        task.category = data['category']

    if 'completed' in data:
        task.completed = bool(data['completed'])

    if 'due_date' in data:
        if data['due_date']:
            try:
                task.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d').date()
            except ValueError:
                pass
        else:
            task.due_date = None

    db.session.commit()
    return jsonify(task.to_dict()), 200

def delete_task(current_user, task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()

    if not task:
        return jsonify({'message': 'Task not found or access denied!'}), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully!'}), 200

def clear_all_tasks(current_user):
    Task.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    return jsonify({'message': 'All user tasks cleared successfully!'}), 200