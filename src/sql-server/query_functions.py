from config import connect_to_db
from config import SERVER, DB, USERNAME, PASSWORD, PORT, DRIVER


conn = connect_to_db(server=SERVER, db=DB, u_name=USERNAME, psswd=PASSWORD, port=PORT, driver=DRIVER)
cursor = conn.cursor()

cursor.execute("SELECT * FROM INFORMATION_SCHEMA.TABLES;")
rows = cursor.fetchall()
print(rows)
