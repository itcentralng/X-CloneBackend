from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_cors import CORS

##-- This is from the model of the file
from dbModel import registraion , login

app = Flask(__name__)
CORS(app)

@app.route("/register", method=["POST"])
async def signup(user_details: registraion ):
    username = user_details.Username
    passwod = user_details.password

    

@app.route("/login" , method=["POST"])
async def login(user_login: login):
    username = user_login.username
    password = user_login.password

    try:

        for i in db_i_will_loop:
            if (username and password in i):
                return {"user Found": 200}
            elif (username in i ):
                return {"invalid password ": 401}
            elif (password in i):
                return {"invalid username ": 402}
            else :
                return {"user cannot be found"}