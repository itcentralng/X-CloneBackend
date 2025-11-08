from flask import Flask


app = Flask()

@app.route("/notification", methods=["GET"])
async def notification():
    return {
        "notification":"coming"
    }