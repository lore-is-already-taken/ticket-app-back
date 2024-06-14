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


####################################################
#   FUNCIONES INSERT
####################################################


def add_user(name: str, email: str, password: str, rol: str) -> int:
    cursor = database_connect().cursor()
    line = f"INSERT INTO Users (name,email,password) VALUES ('{name}','{email}','{password}');"
    cursor.execute(line)
    cursor.commit()

    userID = get_userID_by_email(email)
    add_rol(userID, rol)

    return userID


def add_ticket(autor: int, contenido: str, categoria: str, prioridad: int) -> bool:
    cursor = database_connect().cursor()
    line = f"INSERT INTO Ticket (autor,contenido,categoria,prioridad) VALUES ('{autor}','{contenido}','{categoria}','{prioridad}');"
    cursor.execute(line)
    cursor.commit()
    return True


def add_rol(userID: int, rol: str) -> bool:
    cursor = database_connect().cursor()
    line = f"INSERT INTO Rol (userID,rol) VALUES ('{userID}','{rol}');"
    cursor.execute(line)
    cursor.commit()
    return True


def add_Evento(ticketID: int, contenido: str) -> bool:
    cursor = database_connect().cursor()
    line = (
        f"INSERT INTO Ticket (ticketID,contenido) VALUES ('{ticketID}','{contenido}');"
    )
    cursor.execute(line)
    cursor.commit()
    return True


#####################################################
#   FUNCIONES SELECT
#####################################################


def get_userID_by_email(email: str) -> int:
    """
    Obtiene el userID de un determinado usuario buscandolo
    por email, si no lo encuentra o algo sale mal devuelve 0
    """
    cursor = database_connect().cursor()
    line = f"SELECT userID FROM Users WHERE email='{email}';"
    cursor.execute(line)
    for row in cursor.fetchall():
        return row.userID
    return 0


def get_user_by_ID(id: int) -> List[str]:
    """
    Devuelve un arreglo con 2 elementos [nombre,email].
    Si no encuentra el usuario devuelve un
    arreglo vacio
    """
    cursor = database_connect().cursor()
    line = f"SELECT name,email FROM Users WHERE userID='{id}';"
    cursor.execute(line)
    res = []
    for row in cursor.fetchall():
        row = {"nombre": row.name, "email": row.email}
        res.append(row)
    return res


def get_password_by_email(email: str) -> str:
    """
    Obtiene la contraseña de un usuario segun su email.
    Si no lo encuentra o hubo un error devuelve un string vacio.
    """
    cursor = database_connect().cursor()
    line = f"SELECT password FROM Users WHERE email='{email}';"
    cursor.execute(line)
    for row in cursor.fetchall():
        return row.password
    return ""


def get_tickets_by_autor(userID: int) -> List:
    """
    Obtiene todos los tickets de un determinado autor.
    El formato de retorno es un arreglo de objetos, en el caso de no existir tickets devuelve un arreglo vacio.
    """
    cursor = database_connect().cursor()
    line = f"SELECT rolID FROM Rol WHERE userID='{userID}';"
    cursor.execute(line)
    rolID = ""
    for row in cursor.fetchall():
        rolID = row.rolID

    if rolID == "":
        return []
    line = f"SELECT autor,responsable,contenido,categoria,review,prioridad,textoReview FROM Ticket WHERE autor='{rolID}';"
    cursor.execute(line)
    res = []
    for row in cursor.fetchall():
        tick = {
            "autor": row.autor,
            "resposable": row.resposable,
            "contenido": row.contenido,
            "categoria": row.categoria,
            "prioridad": row.prioridad,
            "review": row.review,
            "textoReview": row.textoReview,
        }
        res.append(tick)
    return res


def get_all_tickets() -> List:
    """
    Obtiene todos los tickets.
    El formato de retorno es un arreglo de objetos, en el caso de no existir tickets devuelve un arreglo vacio.
    """
    cursor = database_connect().cursor()
    line = f"SELECT * FROM Ticket;"
    cursor.execute(line)
    res = []
    for row in cursor.fetchall():
        tick = {
            "autor": row.autor,
            "responsable": row.responsable,
            "contenido": row.contenido,
            "categoria": row.categoria,
            "prioridad": row.prioridad,
            "review": row.review,
            "textoReview": row.textoReview,
        }
        res.append(tick)
    return res


def get_eventos_by_ticketID(ticketID: int) -> List:
    """
    Obtiene todos los eventos relacionados a un ticketID, si no hay ninguno, devuelve un arreglo vacio.
    El retorno de los eventos es dentro de un arreglo de objetos json.
    """
    cursor = database_connect().cursor()
    line = f"SELECT contenido FROM Evento WHERE ticketID='{ticketID}';"
    cursor.execute(line)
    res = []
    for row in cursor.fetchall():
        evento = {"contenido": row.contenido}
        res.append(evento)
    return res


def get_tickets_by_responsable(userID: int) -> List:
    cursor = database_connect().cursor()
    line = f"SELECT rolID FROM Rol WHERE userID='{userID}';"
    cursor.execute(line)
    for row in cursor.fetchall():
        rolID = row.rolID

    line = f"SELECT autor,responsable,contenido,categoria,review,prioridad,textoReview FROM Ticket WHERE responsable='{rolID}';"
    cursor.execute(line)
    res = []
    for row in cursor.fetchall():
        tick = {
            "autor": row.autor,
            "responsable": row.responsable,
            "contenido": row.contenido,
            "categoria": row.categoria,
            "review": row.review,
            "prioridad": row.prioridad,
            "textoReview": row.textoReview
        }
        res.append(tick)
    return res


def get_events_by_userID(userID: int) -> List:
    '''
    A partir de un userID, encuentra el rolID correspondiente, con eso encuentra todos los tickets
    asociados a dicho usuario, desde los cuales extrae los eventos.
    '''
    cursor = database_connect().cursor()
    line = f"SELECT rolID FROM Rol WHERE userID='{userID}';"
    cursor.execute(line)
    if len(cursor.fetchall) == 0:
        return []
    for row in cursor.fetchall():
        rolID = row.rolID

    line = f"SELECT ticketID FROM Ticket WHERE autor='{rolID}';"
    cursor.execute(line)
    if len(cursor.fetchall) == 0:
        return []
    tickets = []
    for row in cursor.fetchall():
            tickets.append(row.ticketID)

    line = f"SELECT contenido FROM Evento WHERE ticketID IN ({tickets});"
    cursor.execute(line)
    eventos = []
    for row in cursor.fetchall():
        evento = {
            "contenido": row.contenido 
        }
        eventos.append(evento)
    return eventos


###############################################################################
#   FUNCIONES UPDATE
###############################################################################


def update_name(usr: int, name: str) -> bool:
    cursor = database_connect().cursor()
    line = f"UPDATE Users SET name='{name}' WHERE userID='{usr}';"
    cursor.execute(line)
    cursor.commit()
    return True


def update_pass(usr: int, oldPassword: str, newPassword: str) -> bool:
    cursor = database_connect().cursor()
    line = f"SELECT password FROM Users WHERE userID='{usr}';"
    cursor.execute(line)
    res = ""
    for row in cursor.fetchall():
        res = row.password
    if res != oldPassword:
        return False

    line = f"UPDATE Users SET password='{newPassword}' WHERE userID='{usr}';"
    cursor.execute(line)
    cursor.commit()
    return True


def asign_responsable(ticket: int, user: int) -> bool:
    '''
    Usando el userID encuentra el rolID correspondiente y lo usa para asignar el valor responsable a 
    un ticket usando el ticketID.
    Devuelve True si la asignacion fue exitosa, y False si no se encontro ningun rol asociado a ese user.
    '''
    cursor = database_connect().cursor()
    line = f"SELECT rolID FROM Rol WHERE userID='{user}';"
    cursor.execute(line)
    rolID = ""
    for row in cursor.fetchall():
        rolID = row.userID
    if rolID == "":
        return False
    line = f"UPDATE Rol SET responsable='{rolID}' WHERE ticketID='{ticket}';"
    cursor.execute(line)
    cursor.commit()
    return True


def delete_user(usr: int) -> bool:
    cursor = database_connect().cursor()
    line = f"DELETE FROM Users WHERE userID='{usr}';"
    cursor.execute(line)
    cursor.commit()
    return True
