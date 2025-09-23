from flask import Flask , request , jsonify

#--for the connection of the db
import psycopg2


#---This is so i can get the values from my .env
import os
from dotenv import load_dotenv

#-- So i can load the env files you know
load_dotenv()

def get_Connection():
     return psycopg2.connect(
         host=str(os.getenv("HOST")),
         dbname=str(os.getenv("DBNAME")),
         user=str(os.getenv("USER")),
         password=os.getenv("PASSWORD"),
         port=str(os.getenv("PORT"))
     )




app = Flask(__name__)


@app.route("/signup" , methods=["POST"])
async def signup():

    conn = get_Connection()
    
    cur = conn.cursor()
    # print(request.get_json())
    # print(request.headers.get("Context-Type"))
    data = request.get_json(force=True, cache=True )
    # return(type(data))

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    try:
        cur.execute("""INSERT INTO testsignup (username , passwordtest , email)
                    VALUES (%s , %s , %s) """, 
                    (username , password ,email ))
        
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"status": "success", "username": username, "email": email})
        
    except Exception as e:
        return (f"fatal Error when inserting {e}")


    

#--- I kept this for so i can use python command to run it ---
if __name__ == "__main__":
    print(os.getenv("HOST"))
    print(os.getenv("DBNAME"))
    print(os.getenv("USER"))
    print(os.getenv("PASSWORD"))
    print(os.getenv("PORT"))
    app.run(debug=True)