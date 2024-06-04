import pyodbc


def database_connect():
    user = "ticket-user"
    password = "computacionapp123.,"

    server = "database-server-ticketapp.database.windows.net"
    database = "ticket-app-database"

    conection_string = "Driver={ODBC Driver 18 for SQL Server};Server=tcp:{},1433;Database={};Uid={};Pwd={};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;".format(
        server, database, user, password
    )
    conn = pyodbc.connect(conection_string)
    return conn
