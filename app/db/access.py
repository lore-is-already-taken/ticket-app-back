from typing import List
import pyodbc

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

    userID = get_userID_by_email(email)
    add_rol(userID,rol)

    return True

def add_ticket(autor:int,contenido:str,categoria:str,prioridad:int)->bool:
    cursor = database_connect().cursor()
    line = f"INSERT INTO Ticket (autor,contenido,categoria,prioridad) VALUES ('{autor}','{contenido}','{categoria}',{prioridad});"
    cursor.execute(line)
    cursor.commit()
    return True

def add_rol(userID:int,rol:str)->bool:
    cursor = database_connect().cursor()
    line = f"INSERT INTO Rol (userID,rol) VALUES ('{userID}','{rol}');"
    cursor.execute(line)
    cursor.commit()
    return True

def add_Evento(ticketID:int,contenido:str)->bool:
    cursor = database_connect().cursor()
    line = f"INSERT INTO Ticket (ticketID,contenido) VALUES ('{ticketID}','{contenido}');"
    cursor.execute(line)
    cursor.commit()
    return True

#####################################################
#   FUNCIONES SELECT
#####################################################

def get_userID_by_email(email:str)->int:
    '''
    Obtiene el userID de un determinado usuario buscandolo
    por email, si no lo encuentra o algo sale mal devuelve 0
    '''
    cursor = database_connect().cursor()
    line = f"SELECT userID FROM Users WHERE email='{email}';"
    cursor.execute(line)
    for row in cursor.fetchcall():
        return row.userID
    return 0

def get_user_by_ID(id:int)->List[str]:
    '''
    Devuelve un arreglo con 2 elementos [nombre,email].
    Si no encuentra el usuario devuelve un
    arreglo vacio
    '''
    cursor = database_connect().cursor()
    line = f"SELECT name,email FROM Users WHERE userID='{id}';"
    cursor.execute(line)
    res = []
    for row in cursor.fetchcall():
        res.append(row.name)
        res.append(row.email)
    return res

def get_password_by_email(email:str)->str:
    '''
    Obtiene la contraseña de un usuario segun su email.
    Si no lo encuentra o hubo un error devuelve un string vacio.
    '''
    cursor = database_connect().cursor()
    line = f"SELECT password FROM Users WHERE email='{email}';"
    cursor.execute(line)
    for row in cursor.fetchcall():
        return row.password
    return ""


def get_tickets_by_autor(userID:int)->List[List[str]]:
    cursor = database_connect().cursor()
    line = f"SELECT rolID FROM Rol WHERE userID='{userID}';"
    cursor.execute(line)
    for row in cursor.fetchcall():
        rolID = row.rolID

    line = f"SELECT autor,responsable,contenido,categoria,review,prioridad,textoReview FROM Ticket WHERE autor='{rolID}';"
    cursor.execute(line)
    res = []
    for row in cursor.fetchcall():
        tick = []
        tick.append(row.autor)
        tick.append(row.responsable)
        tick.append(row.contenido)
        tick.append(row.categoria)
        tick.append(row.review)
        tick.append(row.prioridad)
        tick.append(row.textoReview)
        res.append(tick)
    return res

def get_tickets_by_responsable(userID:int)->List[List[str]]:
    cursor = database_connect().cursor()
    line = f"SELECT rolID FROM Rol WHERE userID='{userID}';"
    cursor.execute(line)
    for row in cursor.fetchcall():
        rolID = row.rolID

    line = f"SELECT autor,responsable,contenido,categoria,review,prioridad,textoReview FROM Ticket WHERE responsable='{rolID}';"
    cursor.execute(line)
    res = []
    for row in cursor.fetchcall():
        tick = []
        tick.append(row.autor)
        tick.append(row.responsable)
        tick.append(row.contenido)
        tick.append(row.categoria)
        tick.append(row.review)
        tick.append(row.prioridad)
        tick.append(row.textoReview)
        res.append(tick)
    return res
