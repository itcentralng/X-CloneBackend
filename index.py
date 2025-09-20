from flask import Flask , jsonify
import datetime as date
app = Flask(__name__)

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