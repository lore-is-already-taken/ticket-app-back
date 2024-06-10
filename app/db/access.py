import pyodbc, struct
from azure import identity

def database_connect():
    user = "volaos"
    password = "corxea-fans420!"

    server = "ticket-api.database.windows.net"
    database = "ticket-api-db"
    odbc = "ODBC Driver 18 for SQL Server"

    conection_string = f"Driver={odbc};Server=tcp:{server},1433;Database={database};Uid={user};Pwd={password};Encrypt=yes;TrustServerCertificate=yes;Connection Timeout=30;"
    try:
        conn = pyodbc.connect(conection_string)
        return conn
    except Exception as e:
        print(e)
database_connect()

####################################################
#   FUNCIONES INSERT
####################################################

def add_user(name:str,email:str,password:str,rol:str)->bool:
    cursor = database_connect().cursor()
    line = f"INSERT INTO Users (name,email,password) VALUES ('{name}','{email}','{password}');"
    cursor.execute(line)
    cursor.commit()
    
    line = f"SELECT userID FROM Users WHERE email='{email}';"
    cursor.execute(line)
    rows = []
    for row in cursor.fetchcall():
        rows.append(f"{row.userID}")

    line = f"INSER INTO Rol (userID,rol) VALUES ('{rows[0]}','{rol}')"
    cursor.execute(line)
    cursor.commit()

    return True

def add_ticket(autor:int,contenido:str,categoria:str,prioridad:int):
    cursor = database_connect().cursor()
    line = f"INSERT INTO Ticket (autor,contenido,categoria,prioridad) VALUES ('{autor}','{contenido}','{categoria}',{prioridad});"
    cursor.execute(line)
    cursor.commit()
    return True

def add_Evento(ticketID:int,contenido:str):
    cursor = database_connect().cursor()
    line = f"INSERT INTO Ticket (ticketID,contenido) VALUES ('{ticketID}','{contenido}');"
    cursor.execute(line)
    cursor.commit()
    return True

#####################################################
#   FUNCIONES SELECT
#####################################################

def get_userID_by_email(email:str):
    cursor = database_connect().cursor()
    line = f"SELECT userID FROM Users WHERE email='{email}';"
    cursor.execute(line)
    for row in cursor.fetchcall():
        return row.userID
