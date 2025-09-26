from flask import Flask , request , jsonify

#--for the connection of the db
import psycopg2


def get_Connection ():
     return psycopg2.connect(
        host="localhost",
        dbname="Xbackenddb",
        user="postgres",
        password="Emmanuel",
        port="5432"
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
        cur.execute("""INSERT INTO testsignupii (username , email , passwordi)
                    VALUES (%s , %s , %s) """, 
                    (username , email , password))
        
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"status": "success", "username": username, "email": email})
        
    except Exception as e:
        return (f"fatal Error when inserting {e}")




@app.route("/login" , methods=["POST"])
async def login():

    conn = get_Connection()

    cur = conn.cursor()

    try:
        data = request.get_json(cache=True , force=True)

        username = data.get("username")
        password = data.get("password")
    
        cur.execute("""SELECT * FROM testsignupii""")
        result = cur.fetchall()
        for i in result:
            if (username and password in i):
                return {"message": 200}
            elif (username in i and password not in i ):
                return {"invalid password ": 401}
            elif (password in i and username not in i):
                return {"invalid username ": 402}
            else :
                return {"user cannot be found"}

        return result


    except Exception as e:
        return (f"fatal Error when inserting {e}")

if __name__ == "__main__":
    app.run(debug=True)