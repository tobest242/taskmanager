from flask import render_template, request, jsonify
from app_config import app, mysql
from models import User

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
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(name, email, password) VALUES(%s, %s, %s)", (name, email, password))
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



# from app import app, db

# # Create the table
# with app.app_context():
#     db.create_all()


if __name__ == '__main__':
    app.run(debug=True)
