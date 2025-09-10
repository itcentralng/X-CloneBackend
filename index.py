from flask import Flask , jsonify;
import datetime
# from flask_cors import CORS;


app = Flask(__name__);
starttime: datetime;

# This is for the statusTime for version and the likes
@app.route("/status" , methods=["GET"])
async def Status():
    Status={
        "status ": "OK",
        "version " :"1.0",
        "upTime": str(datetime.datetime.now() - starttime).capitalize(),
        "timeStamp" : str(datetime.datetime.now()).capitalize(),
    }
    return jsonify(Status);


# CORS(app)
if (__name__ == "__main__"):
    # This is to get the app stateTim and assign it to tiemStamp
    starttime = datetime.datetime.now();
    app.run(debug=True)