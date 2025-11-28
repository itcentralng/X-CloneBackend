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


@app.route("/tweet/like" , methods=["POST"])
async def like():
    data = request.get_json()
    user_id = data.get('user_id')
    tweet_id = data.get('tweet_id')

    if not user_id or not tweet_id:
        return jsonify({'error': 'Missing user_id or item_id'}), 400

    try:
        conn = get_Connection()
        cur = conn.cursor()

        # Insert or update like record
        cur.execute("""
            INSERT INTO like_table (user_id, tweet_id)
            VALUES (%s, %s)
            ON CONFLICT (user_id, tweet_id) DO NOTHING;
        """, (user_id, tweet_id))
        conn.commit()

        
        return jsonify({'message': 'Item liked successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()


@app.route("/tweet/dislike", methods=["POST"])
async def dislike(): 

    data = request.get_json()
    tweet_id = data.get('tweet_id')
    user_id = data.get('user_id')

    if not tweet_id or not user_id:
        return jsonify({'error': 'Missing post_id or user_id'}), 400

    try:
        conn = get_Connection()
        cur = conn.cursor()
        cur.execute("""DELETE FROM dislike_table where id =%s AND tweet_id =%s """, (user_id, tweet_id))
        conn.commit()

        if 'conn' in locals() and conn:
            conn.rollback()

        return jsonify({'message': 'Dislike recorded'}), 200
    

    except Exception as e:
        pass
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()
        cur.close()


if __name__ == "__main__":
    #--- TO run the code so i can debug 
    app.run(debug=True)
    print("X tweets Active")