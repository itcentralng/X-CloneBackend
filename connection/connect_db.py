import psycopg2
import os
from dotenv import load_dotenv


load_dotenv()

#-- This is for the getting the connection
def get_Connection():
        return psycopg2.connect(
            host=str(os.getenv("HOST")),
            dbname=str(os.getenv("DBNAME")),
            user=str(os.getenv("USER")),
            password=os.getenv("PASSWORD"),
            port=str(os.getenv("PORT")),
            sslmode="require"
        )
        