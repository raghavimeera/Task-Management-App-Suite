from flask import request, jsonify, current_app
from database import db
from models.user_model import User
import jwt
import datetime

def register_user():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not name or not email or not password:
        return jsonify({'message': 'All fields are required!'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email address already registered!'}), 400

    new_user = User(name=name, email=email)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully!'}), 201

def login_user():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Email and password are required!'}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return jsonify({'message': 'Invalid credentials!'}), 401

    token = jwt.encode({
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
    }, current_app.config['SECRET_KEY'], algorithm="HS256")

    return jsonify({
        'message': 'Login successful!',
        'token': token,
        'user': user.to_dict()
    }), 200

def get_current_user(current_user):
    return jsonify({'user': current_user.to_dict()}), 200
