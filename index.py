from flask import Flask , jsonify
import datetime as date
app = Flask(__name__)

startTime: date = date.datetime.now()

@app.route("/status" , methods=["GET"])
async def status():
    status={
        "status":"OK",
        "version":"1.0",
        "uptime": str(date.datetime.now() - startTime),
        "timestamp": str(date.datetime.now())
    }

    return jsonify(status)
