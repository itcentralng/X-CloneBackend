

# X-CloneBackend

This is the backend for the cloning of **X (formally known as Twitter)**.

**Python Version**: 3.11.3 (64-bit or 34-bit)

```
THIS IS THE BACKEND OF THE XCLONE
AND THIS CAN BE USED AS A GUIDE FOR YOU TO UNDERSTAND THE BACKEND
```

---

## Libraries Used

* **Flask**

**Language**: Python

---

## Steps

### **STEP I**

Install the required libraries:

```
pip install -r requirements.txt
```

We need to install the libraries to be able to use the RESTFUL API structures (GET, POST, PATCH, PUT, DELETE).

----------------------------------

### **STEP II**

Import Flask from the flask library and instantiate it with the `app` variable.
You can put any name you want for the variable.

We use `__name__` to get the name of the Python file for the server to run when using VS Code, PyCharm, or any IDE.


app = Flask(__name__)


-----------------------------------

### **STEP III**

In this step, we will use the **decorator** and the **router function** to create RESTful endpoints.

Example:

```
@app.route("/status", methods=["GET"])
```

We added the `/status` path and assigned it the method **GET** since we are only retrieving values and not sending values.

-----------------------------------

### **STEP IV**

Run the file with:

```
flask run ||
flask --app index run 
```

-----------------------------------
## UNITTEST WEEK1
i am using python's pytest library for the unittesting.
I have written a single unittest for the `/status` endpoint
the only thing that i am checking is for a `200` status_code response

