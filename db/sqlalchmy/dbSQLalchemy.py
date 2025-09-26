from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#-- Trying to use psycopg2 to connect to the postgres sql then use flask SqlAlchemy to do stuff
import psycopg2 as psy
from pydantic import BaseModel

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://postgres:Emmanuel@localhost:5432/Xbackenddb"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app=app)

class dbs:
    def select():
        result = db.session.execute("SELECT * FROM xsignup")
        return result
    


dbs.select()




