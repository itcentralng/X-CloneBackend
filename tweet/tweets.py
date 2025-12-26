from flask import Flask, g , request , jsonify, flash, send_from_directory
# from connection.connect_db import get_Connection
import psycopg2
import os
from dotenv import load_dotenv
import uuid
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

#-- This is for the getting the connection
from connection.connect_db import get_Connection

import datetime
load_dotenv()


app = Flask(__name__)


# UPLOAD_FOLDER = os.path.join(app.root_path, "static", "media")
# UPLOAD_FOLDER = os.getenv("UPLOAD_DEST")
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = uuid.uuid4().hex




def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/tweet/create" , methods=["POST"])
def Posting_tweet():
    conn = None
    cur = None
    try:
        conn = get_Connection()

        cur = conn.cursor()
        tweet_id = uuid.uuid4()
        data = request.get_json(cache=True)
        tweeting = data.get("tweeting")
        tweetimage = data.get("tweetimage")


        #--- Incase you deceided to you know 
            #--------This is for the image upload if any
             # check if the post request has the file part
        # urls = []
        # for file in request.files.getlist('file'):
        #     # If the user does not select a file, the browser submits an
        #     # empty file without a filename.
        #     if file.filename == '':
        #         flash('No selected file')
        #         # return jsonify({"Message":"Sorry no selected file"}), 400
        #         continue
            
        #     if file and allowed_file(file.filename):
        #         filename = secure_filename(file.filename)
        #         save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        #         file.save(save_path)
        #         urls.append(f"/imagepicker/{filename}")
        # return jsonify({"status":"success", "message":"image uploaded", "urls":urls}) , 200

        #-- To set the dateTime when post was made
        posttime = datetime.datetime.now()

        cur.execute("""INSERT INTO tweets VALUES(%s,%s,%s,%s)""", 
                                (str(tweet_id),tweeting, posttime, tweetimage))

        conn.commit()

        return jsonify({"Post":f"{str(tweeting)}" , "time":f"{str(posttime)}", "image_url":tweetimage, "tweet_id":str(tweet_id)}), 200

    except psycopg2.IntegrityError as error:
         return jsonify({"error": str(error)}), 400
    except Exception as e:
         return jsonify({"error": f"Error from the tweet Backend: {str(e)}"}), 500
    finally:
        if cur: cur.close()
        if conn: conn.close() 
    


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
    finally:
        cur.close()
        conn.close() 


@app.route("/tweet/like" , methods=["POST"])
def like():
    data = request.get_json()
    user_id = g.user_info['id']
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
        """, (str(user_id), tweet_id))
        conn.commit()

        
        return jsonify({'message': 'Item liked successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()


@app.route("/tweet/dislike", methods=["POST"])
def dislike(): 

    data = request.get_json()
    tweet_id = data.get('tweet_id')
    user_id = g.user_info['id']

    if not tweet_id or not user_id:
        return jsonify({'error': 'Missing post_id or user_id'}), 400

    try:
        conn = get_Connection()
        cur = conn.cursor()
        cur.execute("""DELETE FROM like_table where user_id =%s AND tweet_id =%s """, (str(user_id), tweet_id))
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

# @app.route('/imagepicker/<filename>', methods=["GET"])
# def serve_image(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    # return str(filename)

if __name__ == "__main__":
    #--- TO run the code so i can debug 
    app.run(debug=True)
    print("X tweets Active")