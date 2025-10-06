from db.signupdb import signupdb
import psycopg2
import jwt
import os
from flask import Flask , jsonify,request
import datetime as date
from dotenv import load_dotenv
app = Flask(__name__)


startTime: date = date.datetime.now()
load_dotenv()
def get_Connection():
    return psycopg2.connect(
        host=os.getenv("HOST"),
        dbname=os.getenv("NAME"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
        port=os.getenv("PORT"),
        sslmode="require"
    )

##---- This is to get hold of the db so the code won't be bulky for me to keep up


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

@app.route("/signup" , methods=["POST"])
async def signup():
    result = await signupdb()
    return result

if __name__ == ("__main__"):
    app.run(debug=True)
conn = signupdb.get_Connection()
cur = conn.cursor()  

#Week 2 Task Attahir
@app.route("/users",methods=["GET"])
def user():
    try:

        cur.execute("""SELECT * FROM xsignup""")
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
