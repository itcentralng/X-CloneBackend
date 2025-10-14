import psycopg2
import os
from dotenv import load_dotenv


load_dotenv()

#-- This is for the getting the connection
def get_Connection():
        return psycopg2.connect(
            host=os.getenv("HOST"),
            dbname=os.getenv("DBNAME"),
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
            port=os.getenv("PORT"),
            sslmode="require"
        )