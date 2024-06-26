import time

import jwt
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from starlette.middleware.cors import CORSMiddleware

import app.db.access as db
import app.models.models as models

app = FastAPI()


JWT_SECRET = "please_please_update_me_please"
JWT_ALGORITHM = "HS256"


# app.add_middleware(HTTPSRedirectMiddleware)
conn = db.database_connect()
if conn:
    print("the conection is cool")
else:
    print("not connected to the database")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.get("/")
async def root():
    return {"msg": "Up and running!"}


@app.post("/add_user", tags=["User"])
async def create_user(user: models.User) -> dict[str, str]:
    """
    Crea usuario, en caso de que ya exista un usuario con el correo especificado retorna 0. En el caso
    contrario retorna el token de sesion para logearse con el nuevo usuario.
    {access_token}:0
    """
    try:
        verif = db.get_userID_by_email(user.email)
        if verif != 0:
            # Si verif es distinto de 0 es porque encontro un usuario con ese correo
            raise HTTPException(
                status_code=501, detail="Ya existe un usuario con ese correo"
            )
        result = db.add_user(user.name, user.email, user.password, user.rol)
        if result != "":
            user_id = db.get_userID_by_email(user.email)
            payload = {"user_id": user_id, "expires": time.time() + 600}
            token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
            return {"access_token": token}
        else:
            raise HTTPException(status_code=501, detail="No se pudo ingresar")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/get_admins", tags=["User"])
async def get_admins():
    try:
        res = db.get_admins()
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/notifica", tags=["Evento"])
async def notifica(eventos: models.listaID):
    try:
        res = db.notificado(eventos.ids)
        if res:
            return res
        raise HTTPException(status_code=501, detail="No se pudo marcar como notificado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/get_normal_user", tags=["User"])
async def get_normal_user():
    try:
        res = db.get_normales()
        if res != []:
            return res
        raise HTTPException(status_code=501, detail="No hay usuarios normales")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/drop_user", status_code=200, tags=["User"])
async def drop_user(token: models.onlyToken):
    try:
        userID = jwt.decode(token.access_token, JWT_SECRET, algorithms=[JWT_ALGORITHM])[
            "user_id"
        ]
        if db.delete_user(userID):
            return {"msg": "Success"}
        else:
            raise HTTPException(status_code=501, detail="Error al eliminar usuario")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/assign_ticket", tags=["Ticket"])
async def assign_ticket(info: models.ticket_user):
    """
    Recibe un token de sesion como entrada para asignar un ticket a un determinado usuario.
    El objeto consiste de dos campos:
        - access_token: str
        - ticket_id: int
    """
    try:
        userID = jwt.decode(info.access_token, JWT_SECRET, algorithms=[JWT_ALGORITHM])[
            "user_id"
        ]
        res = db.assign_responsable(userID, info.ticket_id)
        if res == True:
            return {"msg": "Success"}
        raise HTTPException(status_code=501, detail="No se pudo asignar")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/get_events", tags=["Evento"])
async def get_events(token: models.onlyToken):
    try:
        userID = jwt.decode(token.access_token, JWT_SECRET, algorithms=[JWT_ALGORITHM])[
            "user_id"
        ]
        return db.get_events_by_userID(userID)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/close_ticket", tags=["Ticket"])
async def close_ticket(ticket: models.onlyID):
    try:
        if db.close_ticket(ticket.id):
            return {"msg": "Success"}
        raise HTTPException(status_code=501, detail="No se pudo cerrar")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/get_tickets", tags=["Ticket"])
async def get_tickets():
    try:
        result = db.get_all_tickets()
        if result != []:
            return result
        raise HTTPException(status_code=501, detail="No hay tickets")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/get_filtered_tickets", tags=["Ticket"])
async def get_filtered_tickets(input: models.random_string):
    """
    Obtiene todos los tickets sin responsable asignado y correspondientes a una determinada categoria.
    """
    try:
        result = db.filtered_get_tickets(input.input)
        if result != []:
            return result
        raise HTTPException(status_code=501, detail="No hay tickets")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/get_user", tags=["User"])
async def get_user(token: models.onlyToken):
    try:
        usrID = jwt.decode(token.access_token, JWT_SECRET, algorithms=[JWT_ALGORITHM])[
            "user_id"
        ]
        result = db.get_user_by_ID(usrID)
        if result != {}:
            return result
        else:
            raise HTTPException(status_code=501, detail="Token invalido")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/get_user_by_rol", tags=["User"])
async def get_user_by_rol(id: models.onlyID):
    try:
        result = db.get_user_by_rolID(id.id)
        if result != {}:
            return result
        raise HTTPException(status_code=501, detail="Not Found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/update_name", status_code=200, tags=["User"])
async def update_name(user: models.changeName):
    try:
        usrID = jwt.decode(user.access_token, JWT_SECRET, algorithms=[JWT_ALGORITHM])[
            "user_id"
        ]
        res = db.update_name(usrID, user.name)
        if res:
            return {"msg": "Success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/update_pass", status_code=200, tags=["User"])
async def update_pass(user: models.changePass):
    try:
        usrID = jwt.decode(user.access_token, JWT_SECRET, algorithms=[JWT_ALGORITHM])[
            "user_id"
        ]
        res = db.update_pass(usrID, user.oldPass, user.newPass)

        if res:
            return {"msg": "Success"}
        else:
            raise HTTPException(status_code=501, detail="Wrong password")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/get_tickets_by_responsable", tags=["Ticket"])
async def get_tickets_by_responsable(token: models.onlyToken):
    try:
        usrID = jwt.decode(token.access_token, JWT_SECRET, algorithms=[JWT_ALGORITHM])[
            "user_id"
        ]
        result = db.get_tickets_by_responsable(usrID)
        if result != []:
            return result
        raise HTTPException(status_code=501, detail="No tickets")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/get_tickets_by_autor", tags=["Ticket"])
async def get_tickets_by_autor(token: models.onlyToken):
    try:
        usrID = jwt.decode(token.access_token, JWT_SECRET, algorithms=[JWT_ALGORITHM])[
            "user_id"
        ]
        result = db.get_tickets_by_autor(usrID)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/login", tags=["User"])
async def login(user: models.log_User) -> dict[str, str]:
    try:
        result = db.get_password_by_email(user.email)
        if result != user.password:
            return HTTPException(status_code=501, detail=str("Wrong password"))
        user_id = db.get_userID_by_email(user.email)
        payload = {"user_id": user_id}
        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
        return {"access_token": token}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/add_ticket", tags=["Ticket"])
async def create_ticket(ticket: models.Ticket):
    try:
        usrID = jwt.decode(ticket.access_token, JWT_SECRET, algorithms=[JWT_ALGORITHM])[
            "user_id"
        ]
        if ticket.responsable == 0:
            result = db.add_ticket(
                usrID, ticket.contenido, ticket.categoria, ticket.prioridad
            )
            if result:
                return {"msg": "Ticket ingresado"}
            raise HTTPException(status_code=501, detail="No se pudo ingresar")
        else:
            result = db.add_ticket_with_responsable(
                usrID,
                ticket.responsable,
                ticket.contenido,
                ticket.categoria,
                ticket.prioridad,
            )
            if result:
                return {"msg": "Ticket ingresado"}
            raise HTTPException(status_code=501, detail="No se pudo ingresar")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/add_evento")
async def create_evento(evento: models.Evento):
    try:
        result = db.add_Evento(evento.ticketID, evento.contenido)
        if result:
            return {"msg": "Evento ingresado"}
        raise HTTPException(status_code=501, detail="No se puede :/")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, port=8000)
