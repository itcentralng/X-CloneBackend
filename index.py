from flask import Flask , jsonify
import datetime as date
app = Flask(__name__)

startTime: date

@app.route("/status" , methods=["GET"])
async def status():
    status={
        "status":"OK",
        "version":"1.0",
        "uptime": str(date.datetime.now() - startTime),
        "timestamp": str(date.datetime.now())
    }
    return jsonify(status)

if ( __name__ == "__main__" ):

    # -- This is to get the time the backend started
    startTime = date.datetime.now()


    app.run(debug=True)
    print("-----XCLONE-backend JUST STARTED------")