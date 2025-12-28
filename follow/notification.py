from flask import Flask, g , jsonify , request
import datetime 
import psycopg2

app = Flask(__name__)
from connection.connect_db import get_Connection
from index import db_table
from models.dbMigrate import notificationmodel

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
        # read = data.get("donereading")


        notify = notificationmodel(
            id=user_id,
            message=message,
            category=catigory,
            time=str(datetime.datetime.now())
        )
        db_table.session.add(notify)
        db_table.session.commit()

        return jsonify({"message":"Notification added"}), 200
        
    except psycopg2.IntegrityError as error:
        conn.rollback()
        return jsonify({"error": "Nofication already added", "reason": str(error)}), 400

    except Exception as error:
        conn.rollback()
        if "(psycopg2.errors.UniqueViolation) duplicate key value violates unique constraint" in str(error):
            return jsonify({"message": "Notification already added"}), 500
        return jsonify({"error":f"Internal Error: {str(error)}"}) , 500
    # finally:
    #     cur.close()
    #     conn.close()
        