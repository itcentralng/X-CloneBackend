from flask import Flask , jsonify

app = Flask(__name__)


@app.route("/" , methods=["GET"])
async def welcome():
    return("Welcome To Testing Section")

@app.route("/testlogin/<username>/<password>" , methods=["GET"])
async def login(username, password):
    userdetails={
        "name ": f"{username}",
        "age ":10,
        "password ": f"{password}"
    }
    return jsonify(userdetails)

if __name__ == "__main__":
    app.run(debug=True);