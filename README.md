```THIS IS THE BACKEND OF THE XCLONE``
AND THIS CAN BE USE AS A GUIDE FOR YOU TO UNDERSTAND THE BACKEND


LIBARY USED FOR THE BACKEND
**FLASK**
And the Langauge used is Python
**STEPS**

__STEP I__:
pip install flask
***We need to install the Libary to be able to use the RESTFUL api structures and the likes i.e the GET, POST, PATCH , PUT , DELTE ***

__STEP II__:
Imported the Flask from the flask lib and instanciated it with the app varible you can put any name you wish to tough if you want for the varible lol.
The use of the __name__ to you know like get the name of the python file for the server to be able to run when you using vs or pycharm any one you want;
app=Flask(__name__)

__STEP III__:
In this step we would be using the decorator and the router function to some restful stuff and also do some like the GET for the status endpoint when the Flask api just started!
***@app.route("/status" , methods=["GET"])***
So added the status path for and assign it the method get since we are only retriving value not sending value instead so.. Yep 

__STEP IV__:
And erm the 
if command __name__ and "__main__" part is for checking if the name of the file as i said is equal to the main so i update the startdate value to the date and time the flask runs and started and then for the app.run(debug=true) is just to run the flask for me and erm if the debug is just help debug stuff to true 
