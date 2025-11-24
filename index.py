from flask import Flask , jsonify , request 
import datetime as date
from datetime import datetime
import jwt
import psycopg2
import os
from dotenv import load_dotenv
from flask_cors import CORS

app = Flask(__name__)
CORS(app=app , supports_credentials=True)
# from db.connection.connect_db import get_Connection

startTime: date = date.datetime.now()


##---- This is to get hold of the db so the code won't be bulky for me to keep up
from db.signupdb import register
from db.logindb import logindb , token_required

#---- This is to get hold of the profile section
from users.users_profile import profile_fetch

#--- This is to run the tweets endpoint in index
from tweet.tweets import Posting_tweet, tweet_list

load_dotenv()

from connection.connect_db import get_Connection

conn = get_Connection()
cur = conn.cursor()

@app.route("/" , methods=["GET"])
async def Welcome():
    return{"Message ":"Welcome to the X-CloneBackend"}


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
def profile(username: str):
    if request.method == "GET":
        return profile_fetch(username=username)
    elif request.method == "PATCH":
        return ("You will soon patch don't worry")



@app.route("/tweet/create" , methods=["POST"])
@token_required
async def Post_tweet():
    result = await Posting_tweet()
    return result

@app.route("/tweet_list/<username>" , methods=["GET"])
@token_required
async def Get_tweet(username: str):
    result = await tweet_list(username=username)
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
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    if not request.get.headers('Authorization'):
        return jsonify({'Unauthorized Request':404})
    else:
        auth_header = request.get.headers('Authorization')
        jwt_token = auth_header.split()[1]
        payload = jwt.decode(jwt_token,app.config['SECRET_KEY'],algorithms=['HS256'])
        email = payload['email']
        cur.execute("SELECT * FROM x_db WHERE email = %s"(email,))
        user = cur.fetchone()
        
    return jsonify({'User_Info':user})

#WEEK5 & 7 Attahir 
@app.route('/<tweet>/list',methods=['GET'])
def list_tweet(tweet):
    liked_status = False
    cur.execute("SELECT * FROM tweets WHERE tweet_id = %s"(tweet,))
    my_tweet = cur.fetchone()
                            #(username,tweets,t_id,time)
    t_id = my_tweet[2]
    cur.execute("SELECT * FROM likes_table WHERE tweet_id = %s"(tweet,))
    tweet_like = cur.fetchone()
                            #(tweet_id,users_liked,id)
    users_liked = tweet_like[1]
    if t_id in users_liked:
        liked_status = True
    like_count = len(users_liked)
    return jsonify({"Like Count":like_count},
                    {"Like Status":liked_status}
                      
                   )

@app.route('/following/<id>')
def following_id(id):
    cur.execute("SELECT COUNT(following_id) FROM follow_table WHERE users_id = %s"(id,))
    user = cur.fetchone()
    following = user[0]
    return jsonify({"no_of_following":following})
@app.route('/followers/<id>')
def followers_id(id):
    cur.execute("SELECT COUNT(follwers_id) FROM follow_table WHERE users_id = %s"(id,))
    user = cur.fetchone()
    followers = user[0]
    return jsonify({"no_of_followers":followers})
@app.route('/image/<id>')
def get_image(id):
    cur.execute("GET IMAGE STRING")
    image = cur.fetchone()
    image_url = image[0]
    return jsonify({"image_url":image_url})
@app.route('/notification/read')
def not_read():
    cur.execute("SELECT from notification values WHERE read = 1")
    data = cur.fetchall()
    return jsonify({"notifications_read":dict(data)})
cur.close()
conn.close()
# --- I put this back so i can run it with python so i can be reloading
# --- If run flask --app (py) run it won't be reloading if their are any changes in the code

if __name__ == ("__main__"):
    #--- TO run the code so i can debug 
    app.run(debug=True)