from flask import Flask, g , jsonify , request

from connection.connect_db import get_Connection
from psycopg2.errors import UniqueViolation
from index import db_table
from models.dbMigrate import followtable

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

        followein = followtable(
            id=user_id,
            follower_id = follower_id
        )

        db_table.session.add(followein)
        db_table.session.commit()
        
        return jsonify({"Result": "successfull"}), 200

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
        conn.rollback()
        if "(psycopg2.errors.UniqueViolation) duplicate key value violates unique constraint" in str(error):
            return jsonify({"message": "Following user already"}), 500
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

        unfollowing = followtable.query.filter_by(
            id=user_id,
            follower_id=followe_id
        ).first()

        if not unfollowing:
            return jsonify({"error": "Follow not found"}), 404

        db_table.session.delete(unfollowing)
        db_table.session.commit()

        if not unfollowing:
            return {"message":"Unfollow Unsuccessfull"}, 404

        return {"message": "Unfollow sucessfull"}, 200
    except UniqueViolation as e:
        conn.rollback()
        errormessage: str = str(e)
        
        
        return jsonify({
            "error": "UniqueViolation",
            "detail": errormessage  # convert exception to string
        }), 400
    except Exception as error:
        conn.rollback()
        return jsonify({"Error": str(error)}) , 500
    # finally:
    #     conn.close()
    #     cur.close()

