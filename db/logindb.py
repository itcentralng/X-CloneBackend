from flask import Flask , request , jsonify
import psycopg2

app = Flask(__name__)


#-- This is for the getting the connection
def get_Connection():
    return psycopg2.connect(
        host="localhost",
        dbname="Xbackenddb",
        user="postgres",
        password="Emmanuel",
        port="5432"
    )


@app.route("/login" , methods=["POST"])
async def login():
    conn = get_Connection()

    cur = conn.cursor()

    try:
        data = request.get_json(cache=True , force=True)

        username = data.get("username")
        password = data.get("password")
    
        cur.execute("""SELECT * FROM xsignup""")
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
