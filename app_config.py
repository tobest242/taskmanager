from flask import Flask
from flask_mysqldb import MySQL
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import Base
import yaml

app = Flask(__name__)

with open('db.yaml', 'r') as stream:
    db = yaml.load(stream, Loader=yaml.FullLoader)

app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

# Create a SQLAlchemy engine and session
engine = create_engine(f"mysql+mysqldb://{app.config['MYSQL_USER']}:{app.config['MYSQL_PASSWORD']}@{app.config['MYSQL_HOST']}/{app.config['MYSQL_DB']}")
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base.query = db_session.query_property()

import os

# Generate a random secret key
# secret_key = os.urandom(24)
# app.secret_key = secret_key
