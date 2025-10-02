from flask import Flask , request , jsonify
import psycopg2

import jwt

### for the bycrpt
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app=app)

import os
from dotenv import load_dotenv

load_dotenv()

#-- This is for the getting the connection
def get_Connection():
    return psycopg2.connect(
        host=str(os.getenv("HOST")),
        dbname=str(os.getenv("DBNAME")),
        user=str(os.getenv("USER")),
        password=os.getenv("PASSWORD"),
        port=str(os.getenv("PORT"))
    )


@app.route("/login" , methods=["POST"])
async def logindb():
    conn = get_Connection()

    cur = conn.cursor()
    data = request.get_json(force=True, cache=True )

    #--- To get the values of email and password
    email = data.get("email")
    password = data.get("password")

    print("Email",email)
    print("Password",password)


    try:
        data = request.get_json(cache=True , force=True)
    
        cur.execute("""SELECT username FROM testsignupii 
                    WHERE email=%s AND passwordi=%s """,
                        (email , password)
                    )
        result = cur.fetchone()

        
        # return result[0]
        if result :
            return {"Welcome Back :":200}
        elif not result:
            return {"User not found :":404}


    except Exception as e:
        return (f"fatal Error when inserting {e}")
    

if __name__ == "__main__":
    print("Login Backend Started")
    app.run(debug=True)
