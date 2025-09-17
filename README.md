# X-CloneBackend

This is the backend for the cloning of X formally known as Twitter

Python Version (3.11.3) 64bit || 34bit

``THIS IS THE BACKEND OF THE XCLONE`
AND THIS CAN BE USE AS A GUIDE FOR YOU TO UNDERSTAND THE BACKEND

LIBARY USED FOR THE BACKEND
**FLASK**
And the Langauge used is Python
**STEPS**

**STEP I**:
pip install -r requirements.txt
**_We need to install the Libary to be able to use the RESTFUL api structures and the likes i.e the GET, POST, PATCH , PUT , DELTE _**

**STEP II**:
Imported the Flask from the flask lib and instanciated it with the app varible you can put any name you wish to tough if you want for the varible lol.
The use of the **name** to you know like get the name of the python file for the server to be able to run when you using vs or pycharm any one you want;
app=Flask(**name**)

**STEP III**:
In this step we would be using the decorator and the router function to some restful stuff and also do some like the GET for the status endpoint when the Flask api just started!
**_@app.route("/status" , methods=["GET"])\_**
So added the status path for and assign it the method get since we are only retriving value not sending value instead so.. Yep

**STEP IV**:
Run the file with _flask run_ command