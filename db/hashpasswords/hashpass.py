from flask_bcrypt import Bcrypt
from flask import Flask


app = Flask(__name__)

bcrypt = Bcrypt(app=app)

@app.route("/hashpass" , methods=["GET"])
async def hashMe():
    try:
        password = "johnson"
        hashed_password = bcrypt.generate_password_hash(password=password).decode('utf-8')
        compare_password = bcrypt.check_password_hash(hashed_password , password)
        if (compare_password):
            print(True)
            return (f" {hashed_password} True")
        else :
            return "False"
    except Exception as e:
        print(f"This seems to be the error: {e}")
        return (f"This seems to be the error: {e}")



if __name__ == "__main__":
    print("Server started!")
    app.run(debug=True)