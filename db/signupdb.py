from flask import Flask , request , jsonify
import os
from dotenv import load_dotenv
load_dotenv()
#--for the connection of the db
import psycopg2


import datetime as date


# --- This is for the password encryption
from flask_bcrypt import Bcrypt

from pydantic import BaseModel

# from connection import 

#-- This is for the getting the connection

from connection.connect_db import get_Connection
conn = get_Connection()



app = Flask(__name__)
bcrypt = Bcrypt(app=app)

#---------These are the global varibles for the so i can update them incase
class confirmers(BaseModel):
    username: str 
    mail: str 
    password_confirm: str


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
async def register():

    conn = get_Connection()
    
    cur = conn.cursor()
    data = request.get_json(force=True, cache=True )

    inpusername = data.get("username")
    inpdate = data.get("dataofbirth")
    inpemail = data.get("email")
    inppassword = data.get("password")

    emailchecker(inpemail)
    usernamechecker(inpusername)
    passwordcheck(inppassword)

    encryp_pass= bcrypt.generate_password_hash(password=confirmers.password_confirm).decode('utf-8')
    random_id = os.urandom(RANDOM_SIZE)

    if confirmers.username == "" :
        return {"Sorry your username is null": 310}
    elif confirmers.mail == "":
        return {"Sorry your Email is null": 311}
    elif confirmers.password_confirm == "":
        return {"Sorry your Password is null": 312}
    
    try:
        
        mail = confirmers.mail
        cur.execute("""INSERT INTO x_db (id , username , email, dob , passwordacc)
                    VALUES (%s , %s , %s , %s , %s) """, 
                    (random_id , confirmers.username ,mail , inpdate , encryp_pass))

        print("Username:", confirmers.username)
        print("Mail: ", mail)
        print("date: ", date)
        
        conn.commit()
        cur.close()
        conn.close()
        

        return jsonify({"status": "success", "username": confirmers.username, "email": confirmers.mail , "password": encryp_pass})
    
    except psycopg2.IntegrityError as error:
        if "duplicate key value violates unique constraint" in str(error):
            return {"User Email Exist Already": 500}
        else :
            return jsonify({"error": f"Database integrity error: {str(error)}"}), 400
    except Exception as e:
        return jsonify({"error": f"Error from the tweet Backend: {str(e)}"}), 500

  

#--- I kept this for so i can use python command to run it ---
if __name__ == "__main__":
    #--- To get the port from the env
    port = os.getenv('PORT', 5000)
    #--- TO run the code so i can debug 
    app.run(debug=True , host="0.0.0.0" , port=port)