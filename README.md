# Task Management System

This is a simple Flask application for user and task management, including user creation, authentication, task creation, assigning task to users and task retrieval. The application uses Flask, Flask-Bcrypt for password hashing, Flask-Login for user authentication, and MySQL for data storage.


# Getting Started

1. Clone the repository to your local machine:
   git clone https://github.com/tobest242/taskmanager.git

2. Install the required dependencies:
   pip install -r requirements.txt

3. Set up your MySQL database and update the app_config.py file with your database configuration.

4. Create a .env file in the root directory and add the following:
    FLASK_APP=your_app_name.py
    FLASK_ENV=development
    SECRET_KEY=your_secret_key
   Replace your_app_name.py with the name of your main application file.

5. Run the application

# Features

# User Management

Create User: POST /user

  Endpoint for creating a new user.
  Requires name, email, and password in the request body.
  Passwords are hashed before storing in the database.
  Get All Users: GET /user
  
  Retrieves a list of all users.
  Get or Delete User: GET /user/<int:user_id> and DELETE /user/<int:user_id>
  
  Retrieves user details or deletes the user with the specified user_id.
  Requires user authentication.

Authentication
  Login: POST /login
  
  Authenticates a user based on the provided email and password.
  Returns a success message upon successful login.
  Logout: GET /logout
  
  Logs out the currently authenticated user.
  
Task Management
  Create Task: POST /create-tasks
  
  Creates a new task and assigns it to a specified user.
  Requires authentication.
  Requires title, description, due_date, and assigned_to_user_email in the request body.
  Get User Tasks: GET /tasks
  
  Retrieves tasks assigned to or created by the currently authenticated user.
