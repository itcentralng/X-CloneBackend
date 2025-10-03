from flask import Flask , request , jsonify
import os
from dotenv import load_dotenv
load_dotenv()
#--for the connection of the db
import psycopg2


#---This is so i can get the values from my .env
import os
from dotenv import load_dotenv

#-- So i can load the env files you know
load_dotenv()


# --- This is for the password encryption
from flask_bcrypt import Bcrypt

def get_Connection():
     return psycopg2.connect(
         host=str(os.getenv("HOST")),
         dbname=str(os.getenv("DBNAME")),
         user=str(os.getenv("USER")),
         password=os.getenv("PASSWORD"),
         port=str(os.getenv("PORT"))
     )




app = Flask(__name__)
bcrypt = Bcrypt(app=app)


@app.route("/signup" , methods=["POST"])
async def signupdb():

    conn = get_Connection()
    
    cur = conn.cursor()
    # print(request.get_json())
    # print(request.headers.get("Context-Type"))
    data = request.get_json(force=True, cache=True )
    # return(type(data))

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    encryp_pass= bcrypt.generate_password_hash(password=password).decode('utf-8')

    try:
        cur.execute("""INSERT INTO testsignupii (username , email , passwordi)
                    VALUES (%s , %s , %s) """, 
                    (username , email , encryp_pass))
        
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"status": "success", "username": username, "email": email , "password": encryp_pass})
        
    except Exception as e:
        return (f"fatal Error when inserting {e}")

  

#--- I kept this for so i can use python command to run it ---
if __name__ == "__main__":
    app.run(debug=True)