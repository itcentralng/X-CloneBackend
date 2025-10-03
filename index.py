import dotenv
import psycopg2
import os
from flask import Flask , jsonify,request
import datetime as date
app = Flask(__name__)


startTime: date = date.datetime.now()
os.load_dotenv()
def get_Connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )

##---- This is to get hold of the db so the code won't be bulky for me to keep up
from db import signupdb

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
    signupdb
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
import jwt
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
    auth_header = request.get.headers('Authorization')
    jwt_token = auth_header.split()[1]
    payload = jwt.decode(jwt_token,app.config['SECRET_KEY'],algorithms=['HS256'])
    email = payload['email']
    cur.execute(f"SELECT * FROM xsignup WHERE email = {email}")
    user = cur.fetchall()
    return jsonify({'User_Info':user})





cur.close()
conn.close()  
