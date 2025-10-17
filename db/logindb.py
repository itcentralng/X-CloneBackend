from flask import Flask , request , jsonify , make_response 
from pydantic import BaseModel
from functools import wraps

#--- This is for the jwt
import jwt
from datetime import timedelta, timezone , datetime


### for the bycrpt
from flask_bcrypt import Bcrypt

import psycopg2
import os
from dotenv import load_dotenv

#-- This is for the getting the connection
# from connection import connect_db


load_dotenv()

app = Flask(__name__)
bcrypt = Bcrypt(app=app)
app.config['SECRET_KEY'] = str(os.getenv("SECRET_KEY"))


#-- This is for the getting the connection

from connection.connect_db import get_Connection
conn =  get_Connection()
    

class confirmers(BaseModel):
    username: str
    mail: str 
    password_confirm: str
    confirm_hash: str

def emialchecker(email: str):
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
            print(confirmers.username)
        except Exception as e:
            print(f"{e} this is the reason")
            return ""
    else:
        print("This is email is less than < 13 characters")
        return ("Email Not Correct")
    

def passwordcheck(password_check: str):
    if len(password_check) > 3:
        confirmers.password_confirm = password_check
        return {"password correct" :  200}
    else:
        return ("Password must be 8char long!")
    


# Token required decorator 
# This is a function for the jwt verification and decoding

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('jwt_token')

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user_mail = confirmers.mail

            curr = conn.cursor()
            curr.execute("""SELECT * FROM x_db WHERE email=%s""" , 
                         (confirmers.mail))
            user_row = curr.fetchone()
            
            #--- This is to get the payload and give it to jwt
            user_info={
                'username':user_row[1],
                'email':user_row[2],
            }

            if not user_info:
                return jsonify({'message': 'Token payload is missing user detials!'}), 401


        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'User Token Expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'messgae': 'Token is missing'}) , 401
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(user_info, *args, **kwargs)

    return decorated


@app.route("/login" , methods=["POST"])
async def logindb():

    cur = conn.cursor()
    data = request.get_json(force=True, cache=True )

    #--- To get the values of email and password
    email = data.get("email")
    password = data.get("password")


    emialchecker(email=email)
    passwordcheck(password_check=password)

    # print("Password",confirmers.confirm_hash)

    try:
        print("Email",confirmers.mail)

        cur.execute("""SELECT username , passwordacc , email FROM x_db WHERE email=%s""",
                    (confirmers.mail,))
        result = cur.fetchone()
        #--- This is to assign the username to the logged in one
        confirmers.username = result[0]
        confirmers.confirm_hash = result[1]

        token = jwt.encode({
                            'email': confirmers.mail, 
                            'exp': datetime.now(timezone.utc) + timedelta(minutes=45)
                            },
                            app.config['SECRET_KEY'], 
                            algorithm="HS256")
        
        response = make_response(jsonify({'message': 'Login successful'}, 200))
        response.set_cookie('jwt_token', token, 
                            httponly=True, 
                            max_age=2700,
                            secure=True,
                            samesite='Lax')
        
        
        # return token
        
        password_match = bcrypt.check_password_hash(pw_hash=confirmers.confirm_hash , password=confirmers.password_confirm)

        # print("Hashed Password: ", confirmers.confirm_hash)
        if result and password_match:
            conn.commit()
            cur.close()
            conn.close()
            return {
                    'user':{
                    'username':result[0],
                    'email': result[2], 
                    },
                    'Welcome Back':200,
                    'token':token,
                   }

        elif not result or not password_match:
            return {'Wrong User Infomation': 500}
        elif not result:
            return {'User not found':500}
        else :
            return {'Error in backendcodebase': 404}


    except Exception as e:
        # return (f"fatal Error when selecting {e}")
        print("error")

if __name__ == "__main__":
    print("Login Backend Started")
    #--- To get the port from the env
    port = os.getenv('PORT', 5000)
    #--- TO run the code so i can debug 
    app.run(debug=True , host="0.0.0.0" , port=port)
