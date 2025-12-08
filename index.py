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
from tweet.tweets import Posting_tweet, tweet_list, like, dislike

#--- This is for the notification of x and follow
from follow.follow import following, Unfollow
from follow.notification import notification


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
def Post_tweet():
    result = Posting_tweet()
    return result

@app.route("/tweet_list/<username>" , methods=["GET"])
@token_required
async def Get_tweet(username: str):
    result = await tweet_list(username=username)
    return result

@app.route("/tweet/like" , methods=["POST"])
@token_required
def likes():
    result = like()
    return result

@app.route("/tweet/dislike" , methods=["POST"])
@token_required
def dislikes():
    result = dislike()
    return result   

@app.route("/follow", methods=["POST"])
@token_required
def follow():
    result = following()
    return result

@app.route("/unfollow", methods=["POST"])
@token_required
def unfollowing():
    result = Unfollow()
    return result

@app.route("/notification" , methods=["POST"])
@token_required
def x_notification():
    result = notification()
    return result

#Week 2 Task Attahir
@app.route("/users",methods=["GET"])
@token_required
def user():
    try:
        cur.execute("""SELECT * FROM x_db""")
        users = cur.fetchall()
        return jsonify({"users": dict(users)})
    except psycopg2.Error as e:
        return {"error": str(e)}
#Attahir Week 4
@app.route('/users/me',methods=["GET"])
@token_required
def me():
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    if not request.get.headers('Authorization'):
        return jsonify({'Unauthorized Request':404})
    else:
        auth_header = request.get.headers('Authorization')
        jwt_token = auth_header.split()[1]
        payload = jwt.decode(jwt_token,app.config['SECRET_KEY'],algorithms=['HS256'])
        email = payload['email']
        cur.execute("SELECT * FROM x_db WHERE email = %s",(email,))
        user = cur.fetchone()
        
    return jsonify({'User_Info':dict(user)})

#WEEK5 & 7 Attahir 
@app.route('/<tweet>/list',methods=['GET'])
def list_tweet(tweet):
    try:
        tweet = int(tweet)
    except ValueError:
        return jsonify({"error":"invalid Tweet id"}),400
    data = request.get_json()
    user_id = data["user_id"]
    liked_status = False
    try:
        cur.execute("SELECT * FROM tweets WHERE tweet_id = %s",(tweet,))
        my_tweet = cur.fetchone()
                                #(username,tweets,t_id,time)
        if my_tweet is None:
            return jsonify({"error":"Tweet Not Found"}),404
    except Exception as e:
        return jsonify({"Error":"Database Error","Details":str(e)}),500
    try:
        cur.execute("SELECT * FROM likes_table WHERE tweet_id = %s",(tweet,))
        tweet_like = cur.fetchone()
                                #(tweet_id,users_liked,id)
        if tweet_like is not None:
            users_liked = tweet_like[1]
        else:
            users_liked = []
        if user_id in users_liked:
            liked_status = True
        like_count = len(users_liked)
        return jsonify({"Like Count":like_count,"Like Status":liked_status})
    except Exception as e:
        return jsonify({"Error":"Database Error","Details":str(e)}),500

@app.route('/following/<id>')
def following_id(id):
    try:
        user_id = int(id)
    except ValueError:
        return jsonify({"error":"invalid User id"})
    try:
        cur.execute("SELECT COUNT(following_id) FROM follow_table WHERE users_id = %s",(user_id,))
        data = cur.fetchone()
        if data is None:
            return jsonify({"error User id not found"}),404
        following = user[0]
        return jsonify({"no_of_following":following})
    except Exception as e:
        return jsonify({"Error":"Database Error","Details":str(e)}),500
@app.route('/followers/<id>')
def followers_id(id):
    try:
        user_id = int(id)
    except ValueError:
        return jsonify({"error":"invalid User id"})
    try:
        cur.execute("SELECT COUNT(follwers_id) FROM follow_table WHERE users_id = %s",(user_id,))
        data = cur.fetchone()
        if data is None:
            return jsonify({"error User id not found"}),404
        followers = user[0]
        return jsonify({"no_of_followers":followers})
    except Exception as e:
        return jsonify({"Error":"Database Error","Details":str(e)}),500
@app.route('/image/<id>')
def get_image(id):
    try:
        image_id = int(id)
    except ValueError:
        return jsonify({"error":"invalid User id"})
    image_path = "test.png" #Path+id.png
    with open(image_path,"r") as f:
        image = f.read(image_path)
    return jsonify({"image":image})
@app.route('/notification/read')
def not_read():
    try:
        cur.execute("SELECT from notification values WHERE read = 1")
        data = cur.fetchall()
        return jsonify({"notifications_read":dict(data)})
    except Exception as e:
        return jsonify({"Error":"Database Error","Details":str(e)}),500
@app.route('/health')
def health_check():
    try:
        psycopg2.connect(
            host=os.getenv("DBHOST"),
            dbname=os.getenv("DBNAME"),
            user=os.getenv("DBUSER"),
            password=os.getenv("DBPASSWORD"),
            port=os.getenv("DBPORT"),
            sslmode="require"
        )
    except Exception as e:
        return jsonify({"status":"unhealthy",
                        "message":f"DB connection error:{str(e)}"})
cur.close()
conn.close()
# --- I put this back so i can run it with python so i can be reloading
# --- If run flask --app (py) run it won't be reloading if their are any changes in the code

if __name__ == ("__main__"):
    #--- TO run the code so i can debug 
    app.run(debug=True)