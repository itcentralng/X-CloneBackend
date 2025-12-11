from flask import Flask , request , jsonify
from flask_bcrypt import Bcrypt
import os
#--for the connection of the db
import psycopg2


import datetime as date


# --- This is for the password encryption
from flask_bcrypt import Bcrypt


# from connection import 

#-- This is for the getting the connection

from connection.connect_db import get_Connection

import uuid
conn = get_Connection()



app = Flask(__name__)
bcrypt = Bcrypt(app=app)

# UPLOAD_FOLDER = os.path.join(app.root_path, "static", "media")
# UPLOAD_FOLDER_PROFILE = os.getenv("UPLOAD_DEST_PROFILE")
# UPLOAD_FOLDER_COVER = os.getenv("UPLOAD_DEST_COVER")
# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

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
    check : bool
    if len(email) > 13:
        print("Email is more than 13 characters", email)
        if "@" in email and ".com" in email:
            confirmers.mail = email
            check = True
        else :
            check = False
        
        if check:
            print("The email is a valid one" )
        elif not check:
            print("This is not a valid mail")

        try:
            print(confirmers.mail)
        except Exception as e:
            print(f"{e} this is the reason")
            return ""
    else:
        print("This is email is less than < 13 characters")
        return ("Email can't be added")
    
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

    connect = conn
    
    cur = connect.cursor()

    inpusername = request.form.get("username")
    inpdate = str(request.form.get("dataofbirth"))
    inpemail = request.form.get("email")
    inppassword = request.form.get("password")
    

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
    # elif confirmers.password_confirm == "":
    #     return {"Sorry your Password is null": 312}
    

        ##--- This is for the image section
    # profile_url=[]
    # cover_url=[]
    # for file in request.files.getlist('profileimage'):
    #     # If the user does not select a file, the browser submits an
    #     # empty file without a filename.
    #     if file.filename == '':
    #         flash('No selected file')
    #         # return jsonify({"Message":"Sorry no selected file"}), 400
    #         continue
        
    #     if file and allowed_file(file.filename):
    #         filename = secure_filename(file.filename)
    #         save_path = os.path.join(app.config['UPLOAD_FOLDER_PROFILE'], filename)
    #         file.save(save_path)
    #         profile_url.append(f"/profile/{filename}")

    # for file in request.files.getlist('coverimage'):
    #     # If the user does not select a file, the browser submits an
    #     # empty file without a filename.
    #     if file.filename == '':
    #         flash('No selected file')
    #         # return jsonify({"Message":"Sorry no selected file"}), 400
    #         continue
        
    #     if file and allowed_file(file.filename):
    #         filename = secure_filename(file.filename)
    #         save_path = os.path.join(app.config['UPLOAD_FOLDER_COVER'], filename)
    #         file.save(save_path)
    #         cover_url.append(f"/coverimage/{filename}")


    try:
        
        mail = confirmers.mail
        cur.execute("""INSERT INTO x_db (id , username , email, dob , passwordacc, profileimage, coverimage)
                    VALUES (%s , %s , %s , %s , %s, %s, %s) """, 
                    (random_id , confirmers.username ,mail , inpdate , encryp_pass, profile_url, cover_url))

        print("Username:", confirmers.username)
        print("Mail: ", mail)
        print("date: ", date)
        

        return jsonify({"status": "success", "username": confirmers.username, "email": confirmers.mail , "password": encryp_pass})
    
    except psycopg2.IntegrityError as error:
        if "duplicate key value violates unique constraint" in str(error):
            return {"User Email Exist Already": 500}
        else :
            return jsonify({"error": f"Database integrity error: {str(error)}"}), 400
    except Exception as e:
        return jsonify({"error": f"Error from the tweet Backend: {str(e)}"}), 500

    finally:
        try:
            conn.commit()
        except Exception as error:
            return jsonify({"Commit Error 500":"Back"}), 500
  

#--- I kept this for so i can use python command to run it ---
if __name__ == "__main__":
    #--- To get the port from the env
    port = os.getenv('PORT', 5000)
    #--- TO run the code so i can debug 
    app.run(debug=True , host="0.0.0.0" , port=port)