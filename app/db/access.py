from datetime import datetime
from typing import Dict, List

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

def get_event(ticketID: int):
    """
    Retrieves the most recent event associated with a given ticketID.
    Returns a dictionary containing the newest event information.
    """
    try:

        cursor = database_connect().cursor()
        line = "SELECT TOP 1 eventoID, ticketID, contenido FROM Evento WHERE ticketID = ? ORDER BY eventoID DESC"
        cursor.execute(line, (ticketID,))
        
        row = cursor.fetchone()
        return(row.contenido.split('-')[3].strip())
    except (Exception) as error:
        print("Error while connecting to PostgreSQL or executing query:", error)
        return f"An error occurred: {str(error)}"
    # if row:
    #     event = {
    #         "eventoID": row.eventoID,
    #         "ticketID": row.ticketID,
    #         "contenido": row.contenido
    #     }
    #     print(event)
    # else:
    #     return ''  # Return None if no events are found for the given ticketID


def update_event(ticket: int, estado: int, cursor):
    if estado == 1:
        evento = "Ticket creado"
    elif estado == 2:
        evento = "Ticket asignado"
    elif estado == 3:
        evento = "Ticket cerrado"
    else:
        return False

    evento = f"{datetime.now().strftime("%d-%m-%Y %H:%M")} - {evento}"
    line = f"INSERT INTO Evento (contenido,ticketID) VALUES ('{evento}','{ticket}')"
    cursor.execute(line)
    return True

def add_ticket(autor: int, contenido: str, categoria: str, prioridad: int) -> bool:
    cursor = database_connect().cursor()
    line = f"SELECT rolID FROM Rol WHERE userID='{autor}';"
    cursor.execute(line)
    rolID = ""
    for row in cursor.fetchall():
        rolID = row.rolID
    if rolID == "":
        return False
    line = f"INSERT INTO Ticket (autor,contenido,categoria,prioridad) OUTPUT INSERTED.ticketID VALUES ('{rolID}','{contenido}','{categoria}','{prioridad}');"
    cursor.execute(line)
    ticketID = cursor.fetchone()[0]
    if not update_event(ticketID, 1, cursor):
        return False
    cursor.commit()
    return True


def add_ticket_with_responsable(autor: int, responsable:int, contenido: str, categoria: str, prioridad: int) -> bool:
    cursor = database_connect().cursor()
    line = f"SELECT rolID FROM Rol WHERE userID='{autor}';"
    cursor.execute(line)
    autorID = ""
    for row in cursor.fetchall():
        autorID = row.rolID
    if autorID == "":
        return False

    line = f"INSERT INTO Ticket (autor,responsable,contenido,categoria,prioridad) OUTPUT INSERTED.ticketID VALUES ('{autorID}','{responsable}','{contenido}','{categoria}','{prioridad}');"
    cursor.execute(line)
    ticketID = cursor.fetchone()[0]
    if not update_event(ticketID, 1, cursor):
        return False
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
        f"INSERT INTO Evento (ticketID,contenido) VALUES ('{ticketID}','{contenido}');"
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


def get_admins():
    cursor = database_connect().cursor()
    line = "SELECT rolID,userID FROM Rol WHERE rol='admin';"
    cursor.execute(line)
    res = []
    user = []
    for row in cursor.fetchall():
        admin = []
        admin.append(row.rolID)
        admin.append(row.userID)
        user.append(row.userID)
        res.append(admin)

    line = f"SELECT name FROM Users WHERE userID IN ({user});"
    line = line.replace("[", "").replace("]", "")
    cursor.execute(line)
    resFinal = []
    i = 0
    for row in cursor.fetchall():
        admin = {"nombre": row.name, "userID": user[i], "rolID": res[i][0]}
        resFinal.append(admin)
        i=i+1
    return resFinal


def get_normales():
    cursor = database_connect().cursor()
    line = "SELECT rolID,userID FROM Rol WHERE rol='normal';"
    cursor.execute(line)
    res = []
    user = []
    for row in cursor.fetchall():
        admin = []
        admin.append(row.rolID)
        admin.append(row.userID)
        user.append(row.userID)
        res.append(admin)
    if res == []:
        return []

    line = f"SELECT name FROM Users WHERE userID IN ({user});"
    line = line.replace("[", "").replace("]", "")
    print(line)
    cursor.execute(line)
    resFinal = []
    i = 0
    for row in cursor.fetchall():
        admin = {"nombre": row.name, "userID": user[i], "rolID": res[i][0]}
        resFinal.append(admin)
        i=i+1
    return resFinal


def get_():
    cursor = database_connect().cursor()
    line = "SELECT rolID,userID FROM Rol WHERE rol='admin';"
    cursor.execute(line)
    res = []
    user = []
    for row in cursor.fetchall():
        admin = []
        admin.append(row.rolID)
        admin.append(row.userID)
        user.append(row.userID)
        res.append(admin)

    line = f"SELECT name FROM Users WHERE userID IN ({user});"
    line = line.replace("[", "").replace("]", "")
    cursor.execute(line)
    resFinal = []
    i = 0
    for row in cursor.fetchall():
        admin = {"nombre": row.name, "userID": user[i], "rolID": res[i][0]}
        resFinal.append(admin)
    return resFinal


def get_user_by_ID(id: int) -> List[str]:
    """
    Devuelve un arreglo con 2 elementos [nombre,email].
    Si no encuentra el usuario devuelve un
    arreglo vacio
    """
    cursor = database_connect().cursor()
    line = f"SELECT name,email FROM Users WHERE userID='{id}';"
    cursor.execute(line)
    name = ""
    mail = ""
    for row in cursor.fetchall():
        name = row.name
        mail = row.email
    line = f"SELECT rol FROM Rol WHERE userID='{id}';"
    cursor.execute(line)
    user = {}
    for row in cursor.fetchall():
        user = {"nombre": name, "email": mail, "rol": row.rol}
    return user


def get_user_by_rolID(rol: int):
    line = f"SELECT userID,rol FROM Rol WHERE rolID='{rol}';"
    cursor = database_connect().cursor()
    cursor.execute(line)
    userID = 0
    for row in cursor.fetchall():
        userID = row.userID
        nombreRol = row.rol

    user = {}
    if userID == 0:
        return user
    line = f"SELECT name,email FROM Users WHERE userID='{userID}';"
    cursor.execute(line)
    for row in cursor.fetchall():
        user = {"name": row.name, "email": row.email, "rol": nombreRol}
    return user


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
    line = f"SELECT ticketID,autor,responsable,contenido,categoria,review,prioridad,textoReview FROM Ticket WHERE autor='{rolID}';"
    cursor.execute(line)
    res = []
    autores: Dict[int, str] = {}
    for row in cursor.fetchall():
        if not row.autor in autores:
            nombre = get_user_by_rolID(row.autor)["name"]
            autores.update({row.autor: nombre})
        responsable = ""
        if row.responsable == None:
            responsable = "No asignado"
        elif not row.responsable in autores:
            nombre = get_user_by_rolID(row.responsable)["name"]
            autores.update({row.responsable: nombre})
        tick = {
            "ticketID": row.ticketID,
            "autor": autores[row.autor],
            "responsable": responsable if responsable!="" else autores[row.responsable],
            "contenido": row.contenido,
            "categoria": row.categoria,
            "prioridad": row.prioridad,
            "review": row.review,
            "textoReview": row.textoReview,
            "status": get_event(row.ticketID)
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
    autores: Dict[int, str] = {}
    for row in cursor.fetchall():
        if not row.autor in autores:
            nombre = get_user_by_rolID(row.autor)["name"]
            autores.update({row.autor: nombre})
        responsable = ""
        if row.responsable == None:
            responsable = "No asignado"
        elif not row.responsable in autores:
            nombre = get_user_by_rolID(row.responsable)["name"]
            autores.update({row.responsable: nombre})
        tick = {
            "ticketID": row.ticketID,
            "autor": autores[row.autor],
            "responsable": responsable if responsable!="" else autores[row.responsable],
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
    rolID = ""
    for row in cursor.fetchall():
        rolID = row.rolID
    if rolID == "":
        return []

    line = f"SELECT ticketID,autor,responsable,contenido,categoria,review,prioridad,textoReview FROM Ticket WHERE responsable='{rolID}';"
    cursor.execute(line)
    res = []
    autores: Dict[int, str] = {}
    for row in cursor.fetchall():
        if not row.autor in autores:
            nombre = get_user_by_rolID(row.autor)["name"]
            autores.update({row.autor: nombre})
        responsable = ""
        if row.responsable == None:
            responsable = "No asignado"
        elif not row.responsable in autores:
            nombre = get_user_by_rolID(row.responsable)["name"]
            autores.update({row.responsable: nombre})
        tick = {
            "ticketID": row.ticketID,
            "autor": autores[row.autor],
            "responsable": responsable if responsable!="" else autores[row.responsable],
            "contenido": row.contenido,
            "categoria": row.categoria,
            "prioridad": row.prioridad,
            "review": row.review,
            "textoReview": row.textoReview,
        }
        res.append(tick)
    return res


def general_get_tickets(userID: int) -> List:
    """
    Obtiene todos los tickets no asignados y los asignados a un usuario en particular.
    """
    cursor = database_connect().cursor()
    line = f"SELECT rolID FROM Rol WHERE userID='{userID}';"
    cursor.execute(line)
    rolID = ""
    for row in cursor.fetchall():
        rolID = row.rolID
    if rolID == "":
        return []

    line = f"SELECT ticketID,autor,responsable,contenido,categoria,review,prioridad,textoReview FROM Ticket WHERE responsable='{rolID}' OR responsable='';"
    cursor.execute(line)
    res = []
    for row in cursor.fetchall():
        tick = {
            "ticketID": row.ticketID,
            "autor": row.autor,
            "responsable": row.responsable,
            "contenido": row.contenido,
            "categoria": row.categoria,
            "review": row.review,
            "prioridad": row.prioridad,
            "textoReview": row.textoReview,
        }
        res.append(tick)
    return res


def filtered_get_tickets(categoria: str) -> List:
    """
    Obtiene todos los tickets de una determinada categoria, que no esten asignados o asignados a un usuario en particular.
    """
    cursor = database_connect().cursor()
    line = (
        f"SELECT * FROM Ticket WHERE (responsable IS NULL AND categoria='{categoria}');"
    )
    cursor.execute(line)
    res = []
    autores: Dict[int, str] = {}
    for row in cursor.fetchall():
        if not row.autor in autores:
            nombre = get_user_by_rolID(row.autor)["name"]
            autores.update({row.autor: nombre})
        responsable = ""
        if row.responsable == None:
            responsable = "No asignado"
        elif not row.responsable in autores:
            nombre = get_user_by_rolID(row.responsable)["name"]
            autores.update({row.responsable: nombre})
        tick = {
            "ticketID": row.ticketID,
            "autor": autores[row.autor],
            "responsable": responsable if responsable!="" else autores[row.responsable],
            "contenido": row.contenido,
            "categoria": row.categoria,
            "prioridad": row.prioridad,
            "review": row.review,
            "textoReview": row.textoReview,
        }
        res.append(tick)
    
    return res


def get_events_by_userID(userID: int) -> List:
    """
    A partir de un userID, encuentra el rolID correspondiente, con eso encuentra todos los tickets
    asociados a dicho usuario, desde los cuales extrae los eventos.
    """
    cursor = database_connect().cursor()
    line = f"SELECT rolID FROM Rol WHERE userID='{userID}';"
    cursor.execute(line)
    rolID = ""
    for row in cursor.fetchall():
        rolID = row.rolID
    if rolID == "":
        return []

    line = f"SELECT ticketID FROM Ticket WHERE autor='{rolID}';"
    cursor.execute(line)
    tickets = []
    for row in cursor.fetchall():
        tickets.append(row.ticketID)

    line = f"SELECT contenido FROM Evento WHERE ticketID IN ({tickets});"
    line = line.replace("[", "").replace("]", "")
    cursor.execute(line)
    eventos = []
    for row in cursor.fetchall():
        evento = {"contenido": row.contenido, "ticketID": row.ticketID}
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


def assign_responsable(user: int, ticket: int) -> bool:
    """
    Usando el userID encuentra el rolID correspondiente y lo usa para asignar el valor responsable a
    un ticket usando el ticketID.
    Devuelve True si la asignacion fue exitosa, y False si no se encontro ningun rol asociado a ese user.
    """
    cursor = database_connect().cursor()
    line = f"SELECT rolID FROM Rol WHERE userID='{user}';"
    cursor.execute(line)
    rolID = ""
    for row in cursor.fetchall():
        rolID = row.rolID
    if rolID == "":
        return False

    line = f"UPDATE Ticket SET responsable='{rolID}' WHERE ticketID='{ticket}';"
    cursor.execute(line)
    update_event(ticket, 2, cursor)
    cursor.commit()
    return True


def close_ticket(ticket: int) -> bool:
    cursor = database_connect().cursor()
    if not update_event(ticket, 3, cursor):
        return False
    cursor.commit()
    return True


def delete_user(usr: int) -> bool:
    cursor = database_connect().cursor()
    line = f"SELECT rolID FROM Rol WHERE userID='{usr}';"
    cursor.execute(line)
    rolID = ""
    for row in cursor.fetchall():
        rolID = row.rolID

    line = f"DELETE FROM Rol WHERE rolID={rolID};"
    cursor.execute(line)
    cursor.commit()
    line = f"DELETE FROM Users WHERE userID={usr};"
    cursor.execute(line)
    cursor.commit()
    return True
