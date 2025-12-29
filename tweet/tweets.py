from flask import Flask, g , request , jsonify, flash, send_from_directory
# from connection.connect_db import get_Connection
import psycopg2
import os
from dotenv import load_dotenv
import uuid
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

#-- This is for the getting the connection
# from connection.connect_db import get_Connection

from index import db_table
from models.dbMigrate import tweets , like_table 

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
    
    try:
        
        tweet_id = uuid.uuid4()
        data = request.get_json(cache=True)
        username = data.get("username")
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

        tweetin = tweets(
            tweet_id=str(tweet_id),
            username=username,
            tweeting=tweeting,
            posttime=posttime,
            tweetimage=tweetimage
        )

        db_table.session.add(tweetin)
        db_table.session.commit()

        return jsonify({"Post":f"{str(tweeting)}" , "time":f"{str(posttime)}", "image_url":tweetimage, "tweet_id":str(tweet_id)}), 200

    except psycopg2.IntegrityError as error:
        db_table.session.rollback()
        return jsonify({"error": str(error)}), 400
    except Exception as e:
        db_table.session.rollback()
        return jsonify({"error": f"Error from the tweet Backend: {str(e)}"}), 500


@app.route("/tweet_list/<username>", methods=["GET"])
def tweet_list(username):
    try:

        limit_param = request.args.get("limit", default=10, type=int)
        id = g.user_info['id']

        try:
            limits = int(limit_param)
        except (TypeError, ValueError):
            limits = 10

        tweetin = db_table.session.query(
            tweets.tweet_id,
            tweets.username,
            tweets.tweeting,
            tweets.posttime,
            tweets.tweetimage,

        ).filter(tweets.username == username).order_by(tweets.posttime.desc()).limit(limits).all()

        return jsonify([
                        {
                            "tweet_id": t.tweet_id,
                            "username": t.username,
                            "tweeting": t.tweeting,
                            "posttime": t.posttime,
                            "tweetimage": t.tweetimage
                        }
                        for t in tweetin
                    ]), 200

    except Exception as codeError:
        db_table.session.rollback()
        return jsonify({"Error: ": f"{codeError}"}), 500
    

@app.route("/tweet/like" , methods=["POST"])
def like():
    data = request.get_json()
    user_id = g.user_info['id']
    tweet_id = data.get('tweet_id')

    if not user_id or not tweet_id:
        return jsonify({'error': 'Missing user_id or item_id'}), 400

    try:

        liking = like_table(
            user_id=user_id,
            tweet_id=tweet_id
        )

        db_table.session.add(liking)
        db_table.session.commit()

        return jsonify({'message': 'Item liked successfully'}), 200

    except psycopg2.IntegrityError as error:
        db_table.session.rollback()
        if "duplicate key value violates unique constraint" in str(error):
            return jsonify({"error": "User has already liked this tweet"}), 400

    except Exception as e:
        db_table.session.rollback()
        if "(psycopg2.errors.UniqueViolation) duplicate key value violates unique constraint" in str(e):
            return jsonify({"message": "Tweet liked already"}), 500
        return jsonify({'error': str(e)}), 500

@app.route("/tweet/dislike", methods=["POST"])
def dislike(): 

    data = request.get_json()
    tweet_id = data.get('tweet_id')
    user_id = g.user_info['id']

    if not tweet_id or not user_id:
        return jsonify({'error': 'Missing post_id or user_id'}), 400

    try:
        
        disliking = like_table.query.filter_by(
            user_id=user_id,
            tweet_id=tweet_id
        ).first()

        if not disliking:
            return jsonify({"error": "Like not found"}), 404

        db_table.session.delete(disliking)
        db_table.session.commit()

        return jsonify({'message': 'Dislike recorded'}), 200
    

    except Exception as e:
        db_table.session.rollback()
        return jsonify({'error': str(e)}), 500


# @app.route('/imagepicker/<filename>', methods=["GET"])
# def serve_image(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    # return str(filename)

if __name__ == "__main__":
    #--- TO run the code so i can debug 
    app.run(debug=True)
    print("X tweets Active")