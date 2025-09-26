from pydantic import BaseModel
from flask import request


data = request.get_json(force=True , cache=True)



class signup(BaseModel):
    username: str
    email: str
    password: str

class login(BaseModel):
    username: str
    password: str