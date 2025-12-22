from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv

load_dotenv()

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_CONNECTION")
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db_table = SQLAlchemy(app)
# migrate = Migrate(app, db=db_table)
from index import db_table

class User(db_table.Model):
    __tablename__ = 'x_db'

    id = db_table.Column(db_table.String,  nullable=False)
    username = db_table.Column(db_table.String(256),  nullable=False)
    email = db_table.Column(db_table.String(256), primary_key=True,  nullable=False)
    dob = db_table.Column(db_table.String(128), nullable=False)
    passwordacc = db_table.Column(db_table.String(256), nullable=False)
    profileimage = db_table.Column(db_table.String(256))
    coverimage = db_table.Column(db_table.String(256))


class followtable(db_table.Model):
    __tablename__ = 'follow_table'

    id = db_table.Column(db_table.String,  nullable=False, primary_key=True)
    follower_id = db_table.Column(db_table.String(256) ,  nullable=False)

class notificationmodel(db_table.Model):
    __tablename__ = 'notification'

    id = db_table.Column(db_table.String,  nullable=False, primary_key=True)
    message = db_table.Column(db_table.String(256),  nullable=False)
    category = db_table.Column(db_table.String(128),  nullable=False)
    time = db_table.Column(db_table.String(256),  nullable=False)


class tweets(db_table.Model):
    __tablename__ = 'tweets'

    tweet_id = db_table.Column(db_table.String,  nullable=False, primary_key=True)
    tweeting = db_table.Column(db_table.String(256),  nullable=False)
    posttime = db_table.Column(db_table.String(128),  nullable=False)
    tweetimage = db_table.Column(db_table.String(256))


class like_table(db_table.Model):
    __tablename__ = 'like_table'

    user_id = db_table.Column(db_table.String,  nullable=False, primary_key=True)
    tweet_id = db_table.Column(db_table.String(256),  nullable=False)


