import pyodbc


def database_connect():
    user = "volaos"
    password = "corxea-fans420!"

    server = "database-server-ticketapp.database.windows.net"
    database = "ticket-api-db"

    conection_string = "Driver={ODBC Driver 18 for SQL Server};Server=tcp:{},1433;Database={};UID={};PWD={};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;".format(
        server, database, user, password
    )
    # connection = "Driver={ODBC Driver 18 for SQL Server};Server=tcp:+"server"+,1433;Database=+"database"+;Uid=+"user"+;Pwd=+"password"+;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
    try:
        conn = pyodbc.connect(conection_string)
        print("CONNECTED")
    except Exception as e:
        print(e)
    return conn
database_connect()
