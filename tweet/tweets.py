from flask import Flask , request , jsonify
from connection.connect_db import get_Connection

app = Flask(__name__)

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
    app.run(debug=True)
    print("X tweets Active")