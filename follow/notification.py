from flask import Flask , jsonify , request
import datetime 

app = Flask(__name__)
from connection.connect_db import get_Connection

@app.route("/notification", methods=["GET"])
async def notification():
    try:
        conn = get_Connection()
        cur = conn.cursor()

        # ---The front-end team will pass the notification form the button clicked sir
        data = request.get_json()
        user_id = data.get("users_id")
        message = data.get("message")
        catigory = data.get("catigory")
        read = data.get("donereading")



        result_notify = cur.execute("INSERT INTO notification values(%s, %s , %s, %s)", 
                                    (user_id,message,catigory,read,datetime.datetime.now()));
        conn.commit()

        if result_notify:
            return jsonify({"message":"Notification added"}), 200
        else :
            return jsonify({"message":"error from the adding"}), 404
        

    except Exception as error:
        return jsonify({"erro":f"Internal Error: {error}"}) , 500
    finally:
        cur.close()
        conn.close()