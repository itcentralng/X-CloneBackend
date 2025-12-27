from flask import Flask, g , jsonify , request

from connection.connect_db import get_Connection
from psycopg2.errors import UniqueViolation

app = Flask(__name__)

@app.route("/follow" , methods=["POST"])
def following():

    conn = get_Connection()
    cur = conn.cursor()
    try:
        data = request.get_json() or {}
        user_id = g.user_info['id']
        follower_id = data.get("follower_id")

        if not follower_id:
            return jsonify({"error": "Missing 'follower_id' in request body"}), 400

        

        cur.execute("INSERT INTO follow_table values (%s , %s)", (user_id , follower_id))

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
        return jsonify({"Error": str(error)}), 500

    # finally:
    #     conn.close()
    #     cur.close()

@app.route("/unfollow", methods=["POST"])
def Unfollow():
    try:
        data = request.get_json() or {}
        user_id = g.user_info['id']
        followe_id = data.get("followe_id")

        print('attr:', user_id  , followe_id)

        conn = get_Connection()
        cur = conn.cursor()

        executed = cur.execute("DELETE FROM follow_table WHERE id = %s AND follower_id = %s" ,
                (str(user_id), str(followe_id)))
        print(f"Row deleted: {cur.rowcount}")

        conn.commit()
        # if executed:
        #     return {"message": "Unfollow sucessfull"}, 200
        # elif not executed:
        #     return {"meesage":"Unfollow Unsuccessfull"}, 404

        return {"message": "Unfollow sucessfull"}, 200
    except UniqueViolation as e:
        errormessage: str = str(e)
        
        
        return jsonify({
            "error": "UniqueViolation",
            "detail": errormessage  # convert exception to string
        }), 400
    except Exception as error:
        return jsonify({"Error": str(error)}) , 500
    # finally:
    #     conn.close()
    #     cur.close()

