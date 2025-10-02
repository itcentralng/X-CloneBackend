from flask import Flask , jsonify
import datetime as date
app = Flask(__name__)

startTime: date = date.datetime.now()

##---- This is to get hold of the db so the code won't be bulky for me to keep up
from db.signupdb import register
from db.logindb import logindb

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
    result = await register()
    return result

@app.route("/login" , method=["POST"])
async def login():
    result = await logindb()
    return result


# --- I put this back so i can run it with python so i can be reloading
# --- If run flask --app (py) run it won't be reloading if their are any changes in the code

if __name__ == ("__main__"):
    app.run(debug=True)