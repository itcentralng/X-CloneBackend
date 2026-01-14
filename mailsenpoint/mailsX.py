from flask import Flask , request , jsonify, logging, json
import requests
from flask_mailman import Mail , EmailMessage
import logging

import os
from dotenv import load_dotenv
from index import db_table
from models.dbMigrate import User


load_dotenv() # for reading API key from `.env` file.

app = Flask(__name__)
app.config['MAIL_SERVER'] = os.getenv("MAILSERVER") 
app.config['MAIL_PORT'] = int(os.getenv("SECONDMAILPORT"))  
app.config['MAIL_USE_SSL'] =  True
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = os.getenv("MAILUSERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAILPASSWORD")

print("Mail Configured")


#-- This is for the mail flask_mailman just as the doc says
mail = Mail(app)


#-- This is for the mail connection it's self
# connection = mail.get_connection()

# # Manually open the connection
# connection.open()

import smtplib, ssl
from email.message import EmailMessage
port = os.getenv("PORTII")  # For SSL
smtp_server = os.getenv("SMTP_SERVER2")
username = os.getenv("USERNAMEII")
password = os.getenv("MAILPASSWORD2")



class Confirmers():
    def __init__(self):
        self.username: str = ""
        self.mail: str = ""
        self.password_confirm: str = ""
        self.confirm_hash: str = ""

confirmers = Confirmers()


def emialchecker(email: str):
    check : bool
    if len(email) > 13:
        print("Email is more than 13 characters", email)
        if "@" in email and ".com" in email:
            confirmers.mail = email
            check = True
        else :
            check = False
        
        if check:
            print("The email is a valid one" )
            logging.info("Email validation successful")
        elif not check:
            print("This is not a valid mail")
            logging.error("Invalid Email failed")

        try:
            print(confirmers.username)
        except Exception as e:
            print(f"{e} this is the reason")
            return ""
    else:
        print("This is email is less than < 13 characters")
        return ("Email Not Correct")
    

@app.route("/resetpassword/confirm", methods=["POST"])
def PasswordConfirm():
    
    
    data = request.get_json()
    email = data.get("email")
    emialchecker(email=email)

    msg = EmailMessage()


    html_message = f"""
                    <div style='font-family:Arial, sans-serif; background:#f9f9f9; padding:20px;'>
                        <div style='max-width:600px; margin:auto; background:#ffffff; border:1px solid #ddd; border-radius:8px; padding:24px;'>
                            <h2 style='color:#333; margin-top:0;'>Confirm Your Password</h2>
                            <p style='color:#555; font-size:14px; line-height:1.6;'>
                            To confirm your new password, please click the link below:
                            </p>
                            <p style='text-align:center; margin:24px 0;'>
                            <a href='{{reset_password}}'
                                style='background:#28a745; color:#fff; text-decoration:none; padding:12px 20px; border-radius:4px; font-weight:bold; cursor:pointer;'>
                                Confirm Password
                            </a>
                            </p>
                            <p style='color:#555; font-size:13px; line-height:1.6;'>
                            For security reasons, this link will expire in 30 minutes.
                            </p>
                            <hr style='border:none; border-top:1px solid #eee; margin:24px 0;' />
                        </div>
                    </div>
                    """
    try:
         #---- To check if the email exists in the database
        user = db_table.session.query(
            User.email
        ).filter_by(email=confirmers.mail).first()

        if not user:
            return jsonify({"status":"failed", "Message":"Email not found"}), 404
        
        import requests

        url = "https://api.zeptomail.com/v1.1/email"

        payload = (
            '{'
            '"from": {"address": "%s"},'
            '"to": [{"email_address": {"address": "%s", "name": "X Clone"}}],'
            '"subject": "X Testing mail",'
            '"htmlbody": %s'
            '}'
        ) % (
            os.getenv("FROMMAIL2") or os.getenv("FROMMAIL"),
            email,
            json.dumps(html_message)   
        )

        headers = {
            'accept': "application/json",
            'content-type': "application/json",
            'authorization': ("Zoho-enczapikey %s" % os.getenv('MAILPASSWORD2')),
        }

        response = requests.request("POST", url, data=payload, headers=headers)

        print(response.status_code)
        if response.status_code == 201:
            print("Email sent successfully via ZeptoMail")
            return jsonify({"status": "success"}), 200
        elif response.status_code == 400:
            print("Bad Request - Invalid email format or missing fields")
            return jsonify({"status": "error", "message": "Bad Request"}), 400
        elif response.status_code != 201:
            return jsonify({"status":"Error", "message": response.status_code})
    except Exception as ex:
        logging.error("Mail error: %s", ex, exc_info=True)
        return(f"Mail error: {str(ex)}")

@app.route("/resetpassword/forgotpassword", methods=["POST"])
def PasswordRequest():

    data = request.get_json()
    email = data.get("email")
    emialchecker(email=email)

    msg = EmailMessage()


    html_message = f"""
                    <div style='font-family:Arial, sans-serif; background:#f9f9f9; padding:20px;'>
                        <div style='max-width:600px; margin:auto; background:#ffffff; border:1px solid #ddd; border-radius:8px; padding:24px;'>
                            <h2 style='color:#333; margin-top:0;'>Password Reset Request</h2>
                            <p style='color:#555; font-size:14px; line-height:1.6;'>
                            You requested to reset your password. Click the button below to set a new one.
                            </p>
                            <p style='text-align:center; margin:24px 0;'>
                            <a href='{{confirm_password}}'
                                style='background:#1d9bf0; color:#fff; text-decoration:none; padding:12px 20px; border-radius:4px; font-weight:bold; cursor:pointer;'>
                                Reset Password
                            </a>
                            </p>
                            <p style='color:#555; font-size:13px; line-height:1.6;'>
                            If you didn’t request this, you can ignore this email — your password will remain unchanged.
                            </p>
                            <hr style='border:none; border-top:1px solid #eee; margin:24px 0;' />
                        </div>
                    </div>
                    """
    try:
        print('Sending Mail')
        logging.info("Sending password reset email %s", confirmers.mail)
        #---- To check if the email exists in the database
        user = db_table.session.query(
            User.email
        ).filter_by(email=confirmers.mail).first()

        if not user:
            return jsonify({"status":"failed", "Message":"Email not found"}), 404
        import requests

        url = "https://api.zeptomail.com/v1.1/email"

        payload = (
            '{'
            '"from": {"address": "%s"},'
            '"to": [{"email_address": {"address": "%s", "name": "X Clone"}}],'
            '"subject": "X Testing mail",'
            '"htmlbody": %s'
            '}'
        ) % (
            os.getenv("FROMMAIL2") or os.getenv("FROMMAIL"),
            email,
            json.dumps(html_message) 
        )

        headers = {
            'accept': "application/json",
            'content-type': "application/json",
            'authorization': ("Zoho-enczapikey %s" % os.getenv('MAILPASSWORD2')),
        }

        response = requests.request("POST", url, data=payload, headers=headers)

        print(response.status_code)
        if response.status_code == 201:
            print("Email sent successfully via ZeptoMail")
            return jsonify({"status": "success"}), 200
        elif response.status_code == 400:
            print("Bad Request - Invalid email format or missing fields")
            return jsonify({"status": "error", "message": "Bad Request"}), 400
        elif response.status_code != 201:
            return jsonify({"status":"Error", "message": response.status_code})
     
    except Exception as ex:
        return(f"Mail error: {str(ex)}")


if __name__ == "__main__":
    app.run(debug=True)

