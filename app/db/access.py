import pyodbc, struct
from azure import identity

def database_connect():
    user = "volaos"
    password = "corxea-fans420!"

    # server = "database-server-ticketapp.database.windows.net"
    server = "ticket-api.database.windows.net"
    # database = "ticket-api-db"
    database = "ticket-api-db"
    odbc = "ODBC Driver 18 for SQL Server"

    conection_string = f"Driver={odbc};Server=tcp:{server},1433;Database={database};Uid={user};Pwd={password};Encrypt=yes;TrustServerCertificate=yes;Connection Timeout=30;"
    try:
        conn = pyodbc.connect(conection_string)
        print("CONNECTED!!!!!!")
        return conn
    except Exception as e:
        print(e)
database_connect() 
