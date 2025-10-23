from flask import Flask , request , jsonify
# from connection.connect_db import get_Connection
import psycopg2
import os
from dotenv import load_dotenv

import datetime

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

        #-- To set the dateTime when post was made
        posttime = datetime.datetime.now()

        cur.execute("""INSERT INTO tweets (username , tweets , tweet_id , posttime) 
                                VALUES(%s,%s,%s,%s)""", 
                                (username,tweeting, 1 , posttime))

        conn.commit()

        return jsonify({"Post":f"{tweeting}" , "time":f"{posttime}"}), 200

    except psycopg2.IntegrityError as error:
         return jsonify({"error": f"Database integrity error: {str(error)}"}), 400
    except Exception as e:
         return jsonify({"error": f"Error from the tweet Backend: {str(e)}"}), 500
    


@app.route("/tweet_list/<username>", methods=["POST"])
async def tweet_list(username):
    try:
        conn = get_Connection()
        cur = conn.cursor()

        cur.execute("""SELECT tweets FROM tweets WHERE username=%s""",
                    (username,))
        results =  cur.fetchall()
        return jsonify({"Results": 
                        results}), 200

    except Exception as codeError:
        return jsonify({"Error: ": f"{codeError}"}), 500

if __name__ == "__main__":
    #--- TO run the code so i can debug 
    app.run(debug=True)
    print("X tweets Active")