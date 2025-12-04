from flask import Flask , request , jsonify
from flask_mailman import Mail , EmailMessage
import logging

import os
from dotenv import load_dotenv


load_dotenv() # for reading API key from `.env` file.

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.ethereal.email'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'kory.aufderhar@ethereal.email'
app.config['MAIL_PASSWORD'] = 'SpNhHVqrVaKhzDCZuT'


#-- This is for the mail flask_mailman just as the doc says
mail = Mail(app)


#-- This is for the mail connection it's self
# connection = mail.get_connection()

# # Manually open the connection
# connection.open()


# @app.route("/reset-password/request", methods=["POST"])
# async def PasswordRequest():
#     try:
        

#         if resp.status_code == 200:  # success
#             # logging.info(f"Successfully sent an email to '{to_address}' via Mailgun API.")
#             jsonify ({"Message":f"Successfully sent an email to '{to_address}' via Mailgun API."})
#         else:  # error
#             logging.error(f"Could not send the email, reason: {resp.text}")

#     except Exception as ex:
#         logging.exception(f"Mailgun error: {ex}")

# @app.route("/reset-password/confirm", methods=["POST"])
# async def PasswordConfirm():
#     try:
        

#         if resp.status_code == 200:  # success
#             # logging.info(f"Successfully sent an email to '{to_address}' via Mailgun API.")
#             jsonify ({"Message":f"Successfully sent an email to '{to_address}' via Mailgun API."}), 200
#         else:  # error
#             logging.error(f"Could not send the email, reason: {resp.text}")
#             jsonify ({"Message":f"Could not send the email, reason: {resp.text}"}), 500

#     except Exception as ex:
#         logging.exception(f"Mailgun error: {ex}")


@app.route("/sendmail", methods=["GET"])
def sendingmail():
    try:
        msg = EmailMessage(
            subject="Hello Ethereal",
            body="Forgotten password kindly reset your password ussing the link i will provide",
            to=["andy9@ethereal.email"],
            from_email="joshon@gmail.com"
        )
        msg.send()
        # if msg.send():
        #     return jsonify({"status":"successfull", "Message":"Mail sent successfully"}), 200
        # else: 
        #     return jsonify({"status":"failed","Message":"Failed to send mail"}), 500
        return jsonify({"status":"successfull", "Message":"Mail sent successfully"}), 200
       
    except Exception as e:
        return jsonify({"status":"error","Message":f"Error occured: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)

