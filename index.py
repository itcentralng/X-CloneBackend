from flask import Flask , jsonify , request
import datetime as date
from datetime import datetime
import jwt
import psycopg2
import os
from dotenv import load_dotenv

app = Flask(__name__)
# from db.connection.connect_db import get_Connection

startTime: date = date.datetime.now()


##---- This is to get hold of the db so the code won't be bulky for me to keep up
from db.signupdb import register
from db.logindb import logindb , token_required

#---- This is to get hold of the profile section
from users.users_profile import profile_fetch

#--- This is to run the tweets endpoint in index
from tweet.tweets import Posting_tweet

load_dotenv()

#-- This is for the getting the connection
def get_Connection():
        return psycopg2.connect(
            host=str(os.getenv("HOST")),
            dbname=str(os.getenv("DBNAME")),
            user=str(os.getenv("USER")),
            password=os.getenv("PASSWORD"),
            port=str(os.getenv("PORT"))
        )
conn = get_Connection()
cur = conn.cursor()

@app.route("/" , methods=["GET"])
async def Welcome():
    return{"Message: "+"Welcome to the X-CloneBackend"}


@app.route("/status" , methods=["GET"])
async def status():
    status={
        "status":"OK",
        "version":"1.0",
        "uptime": str(date.datetime.now() - startTime),
        "timestamp": str(date.datetime.now())
    }

    return jsonify(status)

@app.route("/register" , methods=["POST"])
async def signup():
    result = await register()
    return result

@app.route("/login" , methods=["POST"])
async def login():
    result = await logindb()
    return result

#--- This is for the profile route
@app.route("/profile/<username>" , methods=["GET", "PATCH"])
@token_required
async def profile(username: str):
    if request.method == "GET":
        return await profile_fetch(username=username)
    elif request.method == "PATCH":
        return ("You will soon patch don't worry")


@app.route("/tweet/create" , methods=["POST"])
# @token_required
async def Post_tweet():
    result = await Posting_tweet()
    return result



#Week 2 Task Attahir
@app.route("/users",methods=["GET"])
def user():
    try:

        cur.execute("""SELECT * FROM x_db""")
        users = cur.fetchall()
        return jsonify({"users": users})
        
    except psycopg2.Error as e:
        return {"error": str(e)}
#Attahir Week 4

@app.route('/users/me',methods=["GET"])
def me():

    '''
    
    STEP1: Extract and validate JWT Token from auth header
    STEP2: Get user_email from token_payload
    STEP3: Query DB for user_email
    STEP4: Format and return json response with details.
    STEP5: Handle errors
    
    '''
    app.config['SECRET_KEY'] = 'v0gXEKYBouAqIUbw'
    if not request.get.headers('Authorization'):
        return jsonify({'Unauthorized Request':404})
    else:
        auth_header = request.get.headers('Authorization')
        jwt_token = auth_header.split()[1]
        payload = jwt.decode(jwt_token,app.config['SECRET_KEY'],algorithms=['HS256'])
        email = payload['email']
        cur.execute(f"SELECT * FROM xsignup WHERE email = {email}")
        user = cur.fetchall()
    
    return jsonify({'User_Info':user})

#Week5 Attahir 
@app.route('/tweet/list',methods=['GET'])
def alltweet():
    cur.execute("SELECT * FROM tweetlist")
    all_tweets = cur.fetchall()

    return jsonify({"All Tweets":all_tweets})



cur.close()
conn.close()  


# --- I put this back so i can run it with python so i can be reloading
# --- If run flask --app (py) run it won't be reloading if their are any changes in the code

if __name__ == ("__main__"):
    app.run(debug=True)