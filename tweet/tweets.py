from flask import Flask , request , jsonify
# from connection.connect_db import get_Connection
import psycopg2
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

#-- This is for the getting the connection
# from connection.connect_db import get_Connection
#from connection.connect_db import get_Connection
def get_Connection():
        return psycopg2.connect(
            host=os.getenv("DBHOST"),
            dbname=os.getenv("DBNAME"),
            user=os.getenv("DBUSER"),
            password=os.getenv("DBPASSWORD"),
            port=os.getenv("DBPORT"),
            sslmode="require"
        )

@app.route("/tweet/create" , methods=["POST"])
async def Posting_tweet():
    try:
        conn = get_Connection()

        cur = conn.cursor()
        data = request.get_json(force=True, cache=True)
        username = data.get("username")
        tweeting = data.get("tweeting")

        cur.execute("""INSERT INTO tweet_table (username , tweets) 
                                VALUES(%s,%s)""", 
                                (username,tweeting))

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"Post":f"{tweeting}"}), 200

    except psycopg2.IntegrityError as error:
         return {"DB Error": error}
    except Exception as e:
        return {f" Error from the tweet Backend !!{e}"}

if __name__ == "__main__":
    #--- TO run the code so i can debug 
    app.run(debug=True)
    print("X tweets Active")