from flask import Flask , jsonify
import datetime as date
app = Flask(__name__)
import psycopg2
startTime: date = date.datetime.now()

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
    

#Week 2 Task Attahir
@app.route("/users",methods=["GET"])
def user():
    try:
        conn = psycopg2.connect(
            host="localhost",
            dbname="Xbackenddb",
            user="postgres",
            password="Emmanuel",
            port="5432"
        )
        cur = conn.cursor()
        cur.execute("""SELECT * FROM xsignup""")
        users = cur.fetchall()
        return {"users": users}
        cur.close()
        conn.close()
    except psycopg2.Error as e:
        return {"error": str(e)}
