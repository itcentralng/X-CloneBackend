from pydantic import BaseModel
import datetime

from flask import request
##-- This is to get the date like in erm Models
data = request.get_json()

class registraion(BaseModel):

    Username: dat
    dob: datetime
    password: str


class login(BaseModel):
    username: str
    password: str