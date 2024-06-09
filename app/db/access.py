import pyodbc


def database_connect():
    user = "volaos"
    password = "corxea-fans420!"

    server = "database-server-ticketapp.database.windows.net"
    database = "ticket-api-db"
    odbc = "ODBC Driver 18 for SQL Server"

    conection_string = "Driver={};Server=tcp:{},1433;Database={};UID={};PWD={};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;".format(
        odbc, server, database, user, password
    )
    try:
        conn = pyodbc.connect(conection_string)
        print("CONNECTED!!!!!!")
        return conn
    except Exception as e:
        print(e)
database_connect()
