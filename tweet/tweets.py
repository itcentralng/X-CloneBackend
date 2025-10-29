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

        cur.execute("""INSERT INTO tweets (username , tweets , posttime) 
                                VALUES(%s,%s,%s)""", 
                                (username,tweeting, posttime))

        conn.commit()

        return jsonify({"Post":f"{tweeting}" , "time":f"{posttime}"}), 200

    except psycopg2.IntegrityError as error:
         return jsonify({"error": f"Database integrity error: {str(error)}"}), 400
    except Exception as e:
         return jsonify({"error": f"Error from the tweet Backend: {str(e)}"}), 500
    


@app.route("/tweet_list/<username>", methods=["GET"])
async def tweet_list(username):
    try:
        conn = get_Connection()
        cur = conn.cursor()

        limit_param = request.args.get("limit", default=10, type=int)

        try:
            limits = int(limit_param)
        except (TypeError, ValueError):
            limits = 10

        cur.execute("""SELECT username, tweets, tweet_id, posttime FROM tweets  WHERE username=%s order by tweet_id limit %s """,
                    (username,limits,))
        results =  cur.fetchall()
        return jsonify({"Results": results}), 200

    except Exception as codeError:
        return jsonify({"Error: ": f"{codeError}"}), 500


@app.route("/tweet/like" , methods=["PATCH"])
async def like():
    return jsonify({"Like":"This is the like table"}), 200

@app.route("tweet/unlike", methods=["PATCH"])
async def unlike():
    return jsonify({"Unlike":"This is the unlike table"}), 200

if __name__ == "__main__":
    #--- TO run the code so i can debug 
    app.run(debug=True)
    print("X tweets Active")