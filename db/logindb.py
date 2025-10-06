from flask import Flask , request , jsonify
import psycopg2
from dotenv import load_dotenv
import os
app = Flask(__name__)
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
async def login():
    conn = get_Connection()

    cur = conn.cursor()

    try:
        data = request.get_json(cache=True , force=True)

        username = data.get("username")
        password = data.get("password")
    
        cur.execute("""SELECT * FROM testsignup""")
        result = cur.fetchall()
        for i in result:
            if (username and password in i):
                return {"message log in successfull": 200}
            elif (username in i ):
                return {"invalid password ": 401}
            elif (password in i):
                return {"invalid username ": 402}
            else :
                return {"user cannot be found"}


    except Exception as e:
        return (f"fatal Error when inserting {e}")
