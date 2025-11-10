from flask import Flask , jsonify , request

from connection.connect_db import get_Connection

app = Flask()

@app.route("/follow/<users_id>" , methods=["POST"])
async def following(user_id):
    try:
        data = request.get_json()
        follower_id = data.get("follower_id")

        if not follower_id:
            return jsonify({"error": "Missing 'follower_id' in request body"}), 400

        conn = get_Connection()
        cur = conn.cursor()

        results = cur.execute("INSERT INTO followTable values (%s , %s)", (user_id , follower_id))

        conn.commit()

        if results:
            return jsonify({"Result": results}), 200
        elif not results:
            return jsonify({"Error"}), 404

    except Exception as error:
        return jsonify({"Error": error}), 500
    finally:
        conn.close()
        cur.close()

@app.route("/unfollow/<users_id>")
async def Unfollow(users_id):
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

