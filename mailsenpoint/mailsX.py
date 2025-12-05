from flask import Flask , request , jsonify
from flask_mailman import Mail , EmailMessage
import logging

import os
from dotenv import load_dotenv


load_dotenv() # for reading API key from `.env` file.

app = Flask(__name__)
app.config['MAIL_SERVER'] = os.getenv("MAILSERVER") 
app.config['MAIL_PORT'] = int(os.getenv("MAILPORT"))  
app.config['MAIL_USE_SSL'] =  True
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = os.getenv("MAILUSERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAILPASSWORD")


#-- This is for the mail flask_mailman just as the doc says
mail = Mail(app)


#-- This is for the mail connection it's self
# connection = mail.get_connection()

# # Manually open the connection
# connection.open()


@app.route("/resetpassword/forgotpassword", methods=["POST"])
async def PasswordRequest():
    
    data = request.get_json()
    email = data.get("email")

    html_message = f"""
                    <div style='font-family:Arial, sans-serif; background:#f9f9f9; padding:20px;'>
                        <div style='max-width:600px; margin:auto; background:#ffffff; border:1px solid #ddd; border-radius:8px; padding:24px;'>
                            <h2 style='color:#333; margin-top:0;'>Confirm Your Password</h2>
                            <p style='color:#555; font-size:14px; line-height:1.6;'>
                            To confirm your new password, please click the link below:
                            </p>
                            <p style='text-align:center; margin:24px 0;'>
                            <a href='{{confirm_link}}'
                                style='background:#28a745; color:#fff; text-decoration:none; padding:12px 20px; border-radius:4px; font-weight:bold; cursor:pointer;'>
                                Confirm Password
                            </a>
                            </p>
                            <p style='color:#555; font-size:13px; line-height:1.6;'>
                            For security reasons, both links will expire in {{expiry_hours}} hours.
                            </p>
                            <hr style='border:none; border-top:1px solid #eee; margin:24px 0;' />
                        </div>
                    </div>
                    """
    try:
        msg = EmailMessage(
            subject='X clone Password Reset',
            body=html_message,
            to=[f'{str(email)}'],
            from_email='x@gmail.com'
        )
        msg.content_subtype = "html"
        msg.send()
        if msg.send():
            return jsonify({"status":"successfull", "Message":"Mail sent successfully"}), 200
        else: 
            return jsonify({"status":"failed","Message":"Failed to send mail"}), 500

    except Exception as ex:
        return(f"Mail error: {str(ex)}")

@app.route("/resetpassword/confirm", methods=["POST"])
def PasswordConfirm():

    data = request.get_json()
    email = data.get("email")

    html_message = f"""
                    <div style='font-family:Arial, sans-serif; background:#f9f9f9; padding:20px;'>
                        <div style='max-width:600px; margin:auto; background:#ffffff; border:1px solid #ddd; border-radius:8px; padding:24px;'>
                            <h2 style='color:#333; margin-top:0;'>Password Reset Request</h2>
                            <p style='color:#555; font-size:14px; line-height:1.6;'>
                            You requested to reset your password. Click the button below to set a new one.
                            </p>
                            <p style='text-align:center; margin:24px 0;'>
                            <a href='{{reset_link}}'
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
        msg = EmailMessage(
            subject='X clone Confirm Password',
            body=html_message,
            to=[f'{str(email)}'],
            from_email='x@gmail.com'
        )
        msg.content_subtype = "html"
        msg.send()
        if msg.send():
            return jsonify({"status":"successfull", "Message":"Mail sent successfully"}), 200
        else: 
            return jsonify({"status":"failed","Message":"Failed to send mail"}), 500
        # return jsonify({"status":"successfull", "Message":"Mail sent successfully"}), 200

    except Exception as ex:
        return(f"Mail error: {str(ex)}")


@app.route("/sendmail", methods=["GET"])
def sendingmail():
    try:
        msg = EmailMessage(
            subject='X clone Forgotten Password Reset',
            body='Forgotten password kindly reset your password ussing the link i will provide',
            to=['aishamuarin@gmail.com'],
            from_email='x@gmail.com'
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

