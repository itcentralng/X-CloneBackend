from flask import Flask , request , jsonify
import requests
import logging

import os
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO) # set log level
load_dotenv() # for reading API key from `.env` file.

# Sandbox API URL format: https://api.mailgun.net/v3/sandbox<ID>.mailgun.org/messages
MAILGUN_API_URL = "https://api.mailgun.net/v3/YOUR_DOMAIN_NAME/messages"
FROM_EMAIL_ADDRESS = "Sender Name xcloneitcentral@gmail.com"

app = Flask()

@app.route("/reset-password/request", methods=[""])
async def PasswordRequest():
    try:
        api_key = os.getenv("MAILGUN_API_KEY")  
        data = request.get_json()
        to_address = data.get("to_address")

        resp = requests.post(MAILGUN_API_URL, auth=("api", api_key),
                             data={"from": FROM_EMAIL_ADDRESS,
                                   "to": to_address, "subject": "Reset Password", "text": "Good Day, Welcome to Reset Password how would you like to me do it"})
        if resp.status_code == 200:  # success
            # logging.info(f"Successfully sent an email to '{to_address}' via Mailgun API.")
            jsonify ({"Message":f"Successfully sent an email to '{to_address}' via Mailgun API."})
        else:  # error
            logging.error(f"Could not send the email, reason: {resp.text}")

    except Exception as ex:
        logging.exception(f"Mailgun error: {ex}")

@app.route("/reset-password/confirm", methods=[""])
async def PasswordConfirm():
    try:
        api_key = os.getenv("MAILGUN_API_KEY")  
        data = request.get_json()
        to_address = data.get("to_address")

        resp = requests.post(MAILGUN_API_URL, auth=("api", api_key),
                             data={"from": FROM_EMAIL_ADDRESS,
                                   "to": to_address, "subject": "Reset Password", "text": "Good Day, Welcome to Confirm X accoutn how would you like to me do it"})
        if resp.status_code == 200:  # success
            # logging.info(f"Successfully sent an email to '{to_address}' via Mailgun API.")
            jsonify ({"Message":f"Successfully sent an email to '{to_address}' via Mailgun API."}), 200
        else:  # error
            logging.error(f"Could not send the email, reason: {resp.text}")
            jsonify ({"Message":f"Could not send the email, reason: {resp.text}"}), 500

    except Exception as ex:
        logging.exception(f"Mailgun error: {ex}")