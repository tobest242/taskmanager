from flask import Flask
from flask_mysqldb import MySQL
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import Base
import os

app = Flask(__name__)


from dotenv import load_dotenv
load_dotenv()

app.config['MYSQL_HOST'] = os.environ.get('mysql_host')
app.config['MYSQL_USER'] = os.environ.get('mysql_user')
app.config['MYSQL_PASSWORD'] = os.environ.get('mysql_password')
app.config['MYSQL_DB'] = os.environ.get('mysql_db')

mysql = MySQL(app)

# Create a SQLAlchemy engine and session
engine = create_engine(f"mysql+mysqldb://{app.config['MYSQL_USER']}:{app.config['MYSQL_PASSWORD']}@{app.config['MYSQL_HOST']}/{app.config['MYSQL_DB']}")
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base.query = db_session.query_property()

import os

#random secret key
secret_key = os.urandom(24)
app.secret_key = secret_key