from flask import Flask, g , jsonify , request
import datetime 
import psycopg2

app = Flask(__name__)
from connection.connect_db import get_Connection

@app.route("/notification", methods=["GET"])
def notification():
    try:
        conn = get_Connection()
        cur = conn.cursor()

        # ---The front-end team will pass the notification form the button clicked sir
        data = request.get_json()
        user_id = g.user_info['id']
        message = data.get("message")
        catigory = data.get("catigory")
        read = data.get("donereading")



        cur.execute("INSERT INTO notification values(%s, %s , %s, %s, %s)", 
                                    (str(user_id),message,catigory,read,str(datetime.datetime.now())));
        conn.commit()

        if cur.rowcount +1:
            return jsonify({"message":"Notification added"}), 200
        else:
            return jsonify({"message":"error from the adding"}), 404
        
    except psycopg2.IntegrityError as error:
         return jsonify({"error": "Nofication already added"}), 400
    
    except Exception as error:
        return jsonify({"error":f"Internal Error: {str(error)}"}) , 500
    finally:
        cur.close()
        conn.close()
        