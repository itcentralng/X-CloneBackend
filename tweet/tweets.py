from flask import Flask , request , jsonify
# from connection.connect_db import get_Connection
import psycopg2
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

#-- This is for the getting the connection
# from connection.connect_db import get_Connection
from connection.connect_db import get_Connection


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
         return jsonify({"error": f"Database integrity error: {str(error)}"}), 400
    except Exception as e:
         return jsonify({"error": f"Error from the tweet Backend: {str(e)}"}), 500

if __name__ == "__main__":
    #--- TO run the code so i can debug 
    app.run(debug=True)
    print("X tweets Active")