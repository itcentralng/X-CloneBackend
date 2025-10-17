import psycopg2
import os
from dotenv import load_dotenv


load_dotenv()

#-- This is for the getting the connection
def get_Connection():
        return psycopg2.connect(
            host=os.getenv("DBHOST"),
            dbname=os.getenv("DBNAME"),
            user=os.getenv("DBUSER"),
            password=os.getenv("DBPASSWORD"),
            port=os.getenv("DBPORT"),
            sslmode="require"
        )