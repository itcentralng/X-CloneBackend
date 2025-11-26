from flask import Flask , jsonify , request

from connection.connect_db import get_Connection
from psycopg2.errors import UniqueViolation

app = Flask(__name__)

@app.route("/follow" , methods=["POST"])
def following():

    conn = get_Connection()
    cur = conn.cursor()
    try:
        data = request.get_json() or {}
        user_id = data.get("user_id")
        follower_id = data.get("follower_id")

        if not follower_id:
            return jsonify({"error": "Missing 'follower_id' in request body"}), 400

        

        cur.execute("INSERT INTO followtable values (%s , %s)", (user_id , follower_id))

        conn.commit()
        # print(f"This is results {cur.rowcount > 0}")

        if cur.rowcount > 0:
            return jsonify({"Result": "successfull"}), 200
        elif not cur.rowcount < 0:
            return jsonify({"Error"}), 404

    except UniqueViolation as e:
        errormessage: str = str(e)
        if "duplicate key value violates unique constraint" in errormessage:
            return jsonify({
                "error": "AlreadyFollowing",
                "detail": "You are already following this user."
            }), 400
        
        return jsonify({
            "error": "UniqueViolation",
            "detail": errormessage  # convert exception to string
        }), 400
    except Exception as error:
        return jsonify({"Error": error}), 500

    finally:
        if cur:
            conn.close()
        if conn:
            cur.close()

@app.route("/unfollow/<users_id>", methods=["POST"])
def Unfollow(users_id):
    try:
        data = request.get_json()
        followe_id = data.get("followe_id")

        conn = get_Connection()
        cur = conn.cursor()
        
        results = cur.execute("DELETE FROM followTable WHERE follower_id = %s AND followe_id = %s",
                (users_id, followe_id)
            )

        conn.commit()

        if results:
            return jsonify({"Unfollowed": "Sucessfull" }), 200
        elif not results:
            return jsonify({"Error"}), 404

        
    except Exception as error:
        return jsonify({"Error": error}) , 500
    finally:
        conn.close()
        cur.close()

