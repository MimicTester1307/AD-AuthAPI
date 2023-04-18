import pyodbc
import os
from dotenv import load_dotenv

# load environment variables
load_dotenv()

SERVER = os.environ.get("MSSQL_SERVER")
DB = os.environ.get("MSSQL_DB")
USERNAME = os.environ.get("MSSQL_USER")
PASSWORD = os.environ.get("MSSQL_USER_PSSWD")
PORT = os.environ.get("PORT")
DRIVER = os.environ.get("ODBC_DRIVER")

CONNECTION_STRING = f'Driver={DRIVER};Server=tcp:{SERVER},{PORT};Database={DB};Uid={USERNAME};Pwd={PASSWORD};Encrypt' \
                    f'=yes;TrustServerCertificate=no;Connection Timeout=30;'


def connect_to_db(server, db, u_name, psswd, driver):
    conn = pyodbc.connect(CONNECTION_STRING)
    return conn
