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


def connect_to_db(server, db, u_name, psswd, port, driver):
    connection_string = f'Driver={driver};Server=tcp:{server},{port};Database={db};Uid={u_name};Pwd={psswd};Encrypt' \
                        f'=yes;TrustServerCertificate=no;Connection Timeout=30;'
    conn = pyodbc.connect(connection_string)
    return conn
