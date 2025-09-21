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


    

#--- I kept this for so i can use python command to run it ---
if __name__ == "__main__":
    app.run(debug=True)