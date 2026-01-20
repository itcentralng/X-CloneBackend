from flask import Flask , request , jsonify
from flask_bcrypt import Bcrypt
import os
from dotenv import load_dotenv
#--for the connection of the db
import psycopg2


import datetime as date


# --- This is for the password encryption
from flask_bcrypt import Bcrypt

from flask import g
# from connection import 

#-- This is for the getting the connection
# from connection.connect_db import get_Connection


#--- This is the session for auth signing up
from models.dbMigrate import User , tempcodedb , tempdb

from index import db_table

import uuid
import random

load_dotenv()

app = Flask(__name__)
bcrypt = Bcrypt(app=app)

# UPLOAD_FOLDER = os.path.join(app.root_path, "static", "media")
# UPLOAD_FOLDER_PROFILE = os.getenv("UPLOAD_DEST_PROFILE")
# UPLOAD_FOLDER_COVER = os.getenv("UPLOAD_DEST_COVER")
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# app.config['UPLOAD_FOLDER_PROFILE'] = UPLOAD_FOLDER_PROFILE
# app.config['UPLOAD_FOLDER_COVER'] = UPLOAD_FOLDER_COVER
app.secret_key = uuid.uuid4().hex

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#---------These are the global varibles for the so i can update them incase
class Confirmers:
    def __init__(self):
        self.username: str = ""
        self.mail: str = ""
        self.password_confirm: str = ""

confirmers = Confirmers()
RANDOM_SIZE: int=20

#--- This is the regex function for looping and check if the email ends with @gmail.com
def emailchecker(email: str):
    """
    Validate email and return (bool, message).
    True, None  -> valid
    False, str  -> invalid with error message
    """
    if not email:
        return False, "Email is required"
    if len(email) < 5:
        return False, "Email is too short"
    # basic checks; adapt with regex if needed
    if len(email) > 13 and "@" in email and ".com" in email:
        confirmers.mail = email
        return True, None
    return False, "The email is not a valid one"
    # else:
    #     print("This is email is less than < 13 characters")
    #     return ("Email can't be added")
    
def usernamechecker(username_check: str):
    try:
        if len(username_check) > 4:
            confirmers.username = username_check
            return {"user sucessfull" :  200}
        else:
            return ("This is not a valid username!")
    except:
        return jsonify({"username error: ", 500})
    

def passwordcheck(password_check: str):
    if len(password_check) > 8:
        confirmers.password_confirm = password_check
        return {"password sucessfull" :  200}
    else:
        return ("Password must be 8char long!")



#--- This is where the routing is for the signup
@app.route("/register" , methods=["POST"])
def register():

    data = request.get_json(cache=True)
    inpusername = data.get("username")
    inpdate = str(data.get("dataofbirth"))
    inpemail = data.get("email")
    inppassword = data.get("password")

    profile_url = data.get("profileurl")
    cover_url = data.get("coverurl")
    
    check: bool 
    emailchecker(inpemail)
    usernamechecker(inpusername)
    passwordcheck(inppassword)

    encryp_pass= bcrypt.generate_password_hash(password=inppassword).decode("utf-8")
    random_id = str(uuid.uuid4())
    print("This is the random id", random_id)

    if confirmers.username == "" :
        return {"Sorry your username is null": 310}
    elif confirmers.mail == "":
        return {"Sorry your Email is null": 311}

    otp_gen = random.randint(100000, 999999)
    g['randotp'] = otp_gen

    try:
        print("This is the OTP:", otp_gen)
        mail = confirmers.mail
       
        new_user = tempdb(
            id=random_id,
            username=confirmers.username,
            email=mail,
            dob=inpdate,
            passwordacc=encryp_pass,
            profileimage=profile_url,
            coverimage=cover_url
        )

        db_table.session.add(new_user)
        db_table.session.commit()

        print("Username:", confirmers.username)
        print("Mail: ", mail)
        print("date: ", date)
        
        # conn.commit()

        return jsonify({"status": "success", "username": confirmers.username, "email": confirmers.mail , "password": encryp_pass})
    
    except psycopg2.IntegrityError as error:
        db_table.session.rollback()
        if "duplicate key value violates unique constraint" in str(error):
            return jsonify({"message": "User Email Exist Already"}), 500
        else :
            return jsonify({"error": f"Database integrity error: {str(error)}"}), 400
    except Exception as e:
        db_table.session.rollback()
        ok, msg = emailchecker(inpemail)
        if not ok:
            return jsonify({"message": str(msg)}), 500
        if "(psycopg2.errors.UniqueViolation) duplicate key value violates unique constraint" in str(e):
            return jsonify({"message": "User Email Exist Already"}), 500
        return jsonify({"error": f"Error from the tweet Backend: {str(e)}"}), 500


@app.route("/otp", methods=["POST"])
def otp():
    data = request.get_json()
    user_otp = data.get("otp")

    otp = db_table.session.query(
            tempcodedb.user_mail,
            tempcodedb.user_code
        ).filter(tempcodedb.user_code == user_otp).first()
    
    if user_otp == otp[1] :
        print("This is the user mail: ", otp[0])


        # Erm i did this so i can get the details the users signuped with in the temp db
        user = db_table.session.query(
            tempdb.id,
            tempdb.username,
            tempdb.email,
            tempdb.dob,
            tempdb.passwordacc,
            tempdb.profileimage,
            tempdb.coverimage
        ).filter(tempdb.email == otp[0]).first()

        new_user = User(
            id=user[0],
            username=user[1],
            email=user[2],
            dob=user[3],
            passwordacc=user[4],
            profileimage=user[5],
            coverimage=user[6]
        )

        db_table.session.add(new_user)
        db_table.session.commit()
    else:
        return jsonify({"message": "Invalid OTP!"}), 400

#--- I kept this for so i can use python command to run it ---
if __name__ == "__main__":
    #--- To get the port from the env
    port = os.getenv('PORT', 5000)
    #--- TO run the code so i can debug 
    app.run(debug=True , host="0.0.0.0" , port=port)