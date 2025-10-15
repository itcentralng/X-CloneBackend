from flask import Flask , request , jsonify
# from connection.connect_db import get_Connection
import psycopg2
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()
#-- This is for the getting the connection
from connection.connect_db import get_Connection
conn = get_Connection()


@app.route("/tweet/create" , methods=["POST"])
async def Posting_tweet():
    try:
        cur = conn.cursor()
        data = request.get_json(force=True, cache=True )
        tweeting = data.get("tweeting")

        cur.execute("INSERT INTO tweets values(%s)", 
                    (tweeting,))
        
        cur.close()
        conn.close()

        return jsonify({"status": "success","postadded":f"{tweeting}"} , 200)


    except Exception as e:
        return {f" Error from the tweet Backend !!{e}"}

if __name__ == "__main__":
    #--- To get the port from the env
    port = os.getenv('PORT', 5000)
    #--- TO run the code so i can debug 
    app.run(debug=True , host="0.0.0.0" , port=port)
    print("X tweets Active")