from flask import render_template, request, jsonify
from app_config import app, mysql
from models import User
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
import jwt
from datetime import datetime, timedelta
from flask import abort

SECRET_KEY = '64742873783272872872829829298'


def generate_token(user_id):
    payload = {
        'sub': user_id,
        'exp': datetime.utcnow() + timedelta(days=11)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token


def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        abort(401, description='Token has expired')
    except jwt.InvalidTokenError:
        abort(401, description='Invalid token')





login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

bycrypt = Bcrypt(app)

@app.route('/user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users")
        data = cur.fetchall()
        cur.close()
        return jsonify(data)

    elif request.method == 'POST':
        user_data = request.get_json()
        name = user_data.get('name')
        email = user_data.get('email')
        password = user_data.get('password')

        hashed_password = bycrypt.generate_password_hash(password).decode('utf-8')
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(name, email, password) VALUES(%s, %s, %s)", (name, email, hashed_password))
        mysql.connection.commit()
        cur.close()
        return 'User Created', 201

@app.route('/user/<int:user_id>', methods=['GET', 'DELETE'])
def get_or_delete_user(user_id):
    cur = mysql.connection.cursor()

    if request.method == 'GET':
        cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        data = cur.fetchone()
        cur.close()
        if data:
            return jsonify({'status': 'success', 'message': 'Data retrieved successfully', 'data': data})
        return 'User not found', 404

    elif request.method == 'DELETE':
        cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
        mysql.connection.commit()
        cur.close()
        return 'User deleted', 200


# @app.route('/login', methods=['POST'])
# def login():
#     if request.method == 'POST':
#         user_data = request.get_json()
#         email = user_data.get('email')
#         password = user_data.get('password')

#         user = User.query.filter_by(email=email).first()

#         if user and bycrypt.check_password_hash(user.password, password):
#             login_user(user)
#             return 'Login successful', 200
#         return 'Login failed', 401

# @app.route('/protected', methods=['GET'])
# @login_required
# def protected():
#     if current_user.is_authenticated:
#         return f'Hello, {current_user.name}! This is a protected route.'

# @app.route('/logout', methods=['GET'])
# def logout():
#     logout_user()
#     return 'Logged out', 200


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        user_date = request.get_json()
        email = user_date.get('email')
        password = user_date.get('password')

        user = User.query.filter_by(email=email).first()

        if user and bycrypt.check_password_hash(user.password, password):
            token = generate_token(user.user_id)
            return jsonify({'token': token}), 200
        return 'Login failed', 401
    
from functools import wraps

def jwt_required(fn):
    @wraps(fn)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return 'Token is missing', 401
        user_id = verify_token(token)
        if user_id == 'Token expired':
            abort(401, description='Token has expired')
        if user_id == 'Invalid token':
            abort(401, description='Invalid token')
        kwargs['user_id'] = user_id
        return fn(*args, **kwargs)
    return decorated

@app.route('/protected', methods=['GET'])
def protected():
    if current_user.is_authenticated:
        user = User.query.get(current_user.id)
        return f'Hello, {user.name}! This is a protected route.'
    else:
        return 'You need to login to access this page', 401



if __name__ == '__main__':
    app.run(debug=True)
