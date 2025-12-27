from flask import Flask , request , jsonify
import psycopg2
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

# from connection.connect_db import get_Connection
#-- This is for the getting the connection

from connection.connect_db import get_Connection
conn =  get_Connection()

@app.route("/profile/<username>", methods=["GET", "PATCH"])
def profile_fetch(username):

    cur = conn.cursor()

    try:

        #----- THIS IS TO GET THE USERS THAT EXIST
        if request.method == "GET":
            cur.execute("SELECT * FROM x_db WHERE username=%s",
                        (username,))
            result = cur.fetchone()
            if result:
                return {'data':{
                    "id":result[0],
                    "username":result[1],
                    "email":result[2],
                    "dob":result[3]
                }}, 200
                # return result
            elif not result:
                return {"USER DOES NOT EXIST !": 404}
            
        
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({"reason": str(e)}, 404)
    except Exception as error:
        conn.rollback()
        return jsonify({f"Fatal error at back {error}"}, 500)


@app.route("/profileupdate/<username>", methods=["PATCH"])
def updateProfile(username):

    try:
        cur = conn.cursor()

        cur.execute("UPDATE x_db SET bob=%s SET username=%s SET profileimg=%s WHERE username=%s id=%s",
                    (request.json['email'], username, request.json['id']))
        conn.commit()
        return jsonify({"status":"success", "message":"Profile updated"}), 200

    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({"reason": str(e)}, 404)
    except Exception as error:
        conn.rollback()
        return jsonify({f"Fatal error at back {error}"}, 500)

if __name__ == "__main__":
    #--- To get the port 
    port = os.getenv('PORT', 5000)

    app.run(debug=True ,host="0.0.0.0", port= port)
    print("Profile Section just started!")