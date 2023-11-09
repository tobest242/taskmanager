from flask import render_template, request, jsonify, redirect, url_for
from app_config import app, mysql
from models import User, Task
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

bcrypt = Bcrypt(app)

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

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(name, email, password) VALUES(%s, %s, %s)", (name, email, hashed_password))
        mysql.connection.commit()
        cur.close()
        return 'User Created', 201

@app.route('/user/<int:user_id>', methods=['GET', 'DELETE'])
@login_required
def get_or_delete_user(user_id):
    cur = mysql.connection.cursor()

    if request.method == 'GET':
        if user_id == current_user.user_id:

            cur.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
            data = cur.fetchone()
            cur.close()
            if data:
                return jsonify({'status': 'success', 'message': 'Data retrieved successfully', 'data': data})
            return 'User not found', 404
        return 'Not Authorized', 401

    elif request.method == 'DELETE':
        if user_id == current_user.user_id:
            cur.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
            mysql.connection.commit()
            cur.close()
            return 'User deleted', 200
        return 'Not Authorized', 401

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_data = request.get_json()
        email = user_data.get('email')
        password = user_data.get('password')

        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return 'Successful', 200
        return 'Login failed', 401
    return 'Please log in', 200


@app.route('/protected', methods=['GET'])
@login_required
def protected():
    if current_user.is_authenticated:
        return f'Hello, {current_user.name}! This is a protected route.'

@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return 'Logged out', 200

@app.route('/create-tasks', methods=['POST'])
@login_required
def create_task():
    if request.method == 'POST':
        data = request.get_json()
        title = data.get('title')
        description = data.get('description')
        due_date = data.get('due_date')
        assigned_to_user_email = data.get('assigned_to_user_email')  # Use email for assignment

        # Check if the assigned user exists
        cur = mysql.connection.cursor()
        cur.execute("SELECT user_id FROM users WHERE email = %s", (assigned_to_user_email,))
        assigned_user_id = cur.fetchone()
        print("Assigned user ID:", assigned_user_id)
        cur.close()

        if not assigned_user_id:
            return 'Assigned user not found', 404

        # Create a new task associated with the current user and assigned to another user
        cur = mysql.connection.cursor()
        cur.execute(
    "INSERT INTO tasks (title, description, due_date, user_email, assigned_to_user_email) VALUES (%s, %s, %s, %s, %s)",
    (title, description, due_date, current_user.email, assigned_to_user_email)
)
        mysql.connection.commit()
        cur.close()

        return jsonify({'message': 'Task created and assigned', 'status': 'success'}), 201

    

@app.route('/tasks', methods=['GET'])
@login_required
def get_user_tasks():
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM tasks WHERE assigned_to_user_email = %s OR user_email = %s", (current_user.email, current_user.email))
        tasks = cur.fetchall()
        cur.close()

        if tasks:
            task_list = []
            for task in tasks:
                task_data = {
                    'task_id': task[0],
                    'title': task[1],
                    'description': task[2],
                    'due_date': task[3],
                }
                task_list.append(task_data)

            return jsonify({'status': 'success', 'message': 'Tasks retrieved successfully', 'data': task_list})

        return 'No tasks found for the current user', 404





if __name__ == '__main__':
    app.run(debug=True)

