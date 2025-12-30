from flask import Flask , request , jsonify , g
import psycopg2
import os
from dotenv import load_dotenv
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
load_dotenv()

# from connection.connect_db import get_Connection
#-- This is for the getting the connection

# from connection.connect_db import get_Connection
# conn =  get_Connection()

from index import db_table
from models.dbMigrate import User


@app.route("/userprofile", methods=["GET", "PATCH"])
def profile_fetch():
    try:

        #----- THIS IS TO GET THE USERS THAT EXIST
        if request.method == "GET":
            id = g.user_info['id']

            user_data = db_table.session.query(
                    User.id,
                    User.username,
                    User.email,
                    User.dob,
                    User.profileimage
                ).filter(
                    User.id == id
                ).first()

            if user_data:
                return {'data':{
                    "id":user_data[0],
                    "username":user_data[1],
                    "email":user_data[2],
                    "dob":user_data[3],
                    "profileimage":user_data[4]
                }}, 200
            elif not user_data:
                return {"USER DOES NOT EXIST !"}, 404
            
        if request.method == "PATCH":
        
                data = request.get_json()
                email = data.get("email")
                dob = data.get("dob")
                profileimage = data.get("profileimage")

                user = db_table.session.query(User).filter_by(email=email).first()
                if not user:
                    return jsonify({"status":"failed", "message":"User not found"}), 404

                # update only fields provided
                if email is not None:
                    user.email = email
                if dob is not None:
                    user.dob = dob
                if profileimage is not None:
                    user.profileimage = profileimage

                try:
                    db_table.session.commit()
                except IntegrityError as e:
                    db_table.session.rollback()
                    return jsonify({"status":"failed", "message":"Integrity error", "reason": str(e)}), 409

                return jsonify({"status":"success", "message":"Profile updated"}), 200

    except psycopg2.errors.UniqueViolation as e:
        db_table.session.rollback()
        return jsonify({"reason": str(e)}, 404)
    except Exception as error:
        db_table.session.rollback()
        return jsonify({f"Fatal error at back {str(error)}"}, 500)


@app.route("/profileupdate/<email>", methods=["PATCH"])
def updateProfile(email):

    try:
        data = request.get_json()
        username = data.get("username")
        updatemail = data.get("email")
        dob = data.get("dob")
        profileimage = data.get("profileimage")


        updated = User.query.filter(User.email == email).update({
            User.username: username,
            User.email: updatemail,
            User.dob: dob,
            User.profileimage: profileimage
        }, synchronize_session=False)

        if updated == 0:
            return jsonify({"status":"failed", "message":"User not found"}), 404

        try:
            db_table.session.commit()
        except IntegrityError as e:
            db_table.session.rollback()
            return jsonify({"status":"failed", "message":"Integrity error", "reason": str(e)}), 409

        return jsonify({"status":"success", "message":"Profile updated"}), 200

    except psycopg2.Error as e:
        db_table.session.rollback()
        return jsonify({"reason": str(e)}) , 404
    except Exception as error:
        db_table.session.rollback()
        return jsonify({f"Fatal error at back {str(error)}"}),500

if __name__ == "__main__":
    #--- To get the port 
    port = os.getenv('PORT', 5000)

    app.run(debug=True ,host="0.0.0.0", port= port)
    print("Profile Section just started!")