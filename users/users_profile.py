from flask import Flask , request , jsonify
import psycopg2
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

from connection.connect_db import get_Connection
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
            
        elif request.method == "PATCH":
            return {"working patch section " : 200}
        
        #----- THIS IS TO PATCH SOME USERS
        if request.method == "PATCH":
            return {"Hmmmm Still Patching", 404}
        
    except psycopg2.Error as e:
        return jsonify({e} , 404)


if __name__ == "__main__":
    app.run(debug=True)
    print("Profile Section just started!")