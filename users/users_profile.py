from flask import Flask , request , jsonify
import psycopg2
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

# from connection.connect_db import get_Connection
#-- This is for the getting the connection
def get_Connection():
        return psycopg2.connect(
            host=str(os.getenv("HOST")),
            dbname=str(os.getenv("DBNAME")),
            user=str(os.getenv("USER")),
            password=os.getenv("PASSWORD"),
            port=str(os.getenv("PORT"))
        )
conn =  get_Connection()

@app.route("/profile/<username>", methods=["GET", "PATCH"])
async def profile_fetch(username):

    cur = conn.cursor()

    try:

        #----- THIS IS TO GET THE USERS THAT EXIST
        if request.method == "GET":
            cur.execute("SELECT * FROM testsignupii WHERE username=%s",
                        (username,))
            result = cur.fetchall()
            if result:
                return jsonify(result , 200)
                # return result
            elif not result:
                return {"USER DOES NOT EXIST !": 404}
            
       
        #----- THIS IS TO PATCH SOME USERS
        if request.method == "PATCH":
            return {"Hmmmm Still Patching", 404}
        
    except psycopg2.Error as e:
        return jsonify({e} , 404)
    except Exception as error:
        return jsonify({f"Fatal error at back {error}"}, 500)


if __name__ == "__main__":
    app.run(debug=True)
    print("Profile Section just started!")