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


@app.post("/add_user")
async def create_user(user: models.User) -> dict[str, str]:
    """
    Crea usuario, en caso de que ya exista un usuario con el correo especificado retorna 0. En el caso
    contrario retorna el token de sesion para logearse con el nuevo usuario.
    {access_token}:0/token
    """
    try:
        verif = db.get_userID_by_email(user.email)
        if verif != 0:
            # Si verif es distinto de 0 es porque encontro un usuario con ese correo
            return {"access_token": "0"}
        result = db.add_user(user.name, user.email, user.password, user.rol)
        if result != "":
            usr = models.log_User
            usr.email = user.email
            usr.password = user.password
            user_id = db.get_userID_by_email(usr.email)
            payload = {"user_id": user_id, "expires": time.time() + 600}
            token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
            return {"access_token": token}
        else:
            raise HTTPException(status_code=500, detail="No se pudo ingresar")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/get_tickets")
async def get_tickets():
    try:
        result = db.get_all_tickets()
        if result:
            return result
        else:
            raise HTTPException(status_code=500, detail="No se pudo ingresar")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/get_user")
async def get_user(usr: models.onlyID):
    try:
        result = db.get_user_by_ID(usr.id)
        if result:
            return result
        else:
            raise HTTPException(status_code=500, detail="No se pudo ingresar")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/update_name", status_code=200)
async def update_name(user: models.changeName):
    try:
        usrID = jwt.decode(user.access_token, JWT_SECRET, algorithms=[JWT_ALGORITHM])['user_id']
        res = db.update_name(usrID,user.name)
        if res:
            return {"msg": "Success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/update_pass", status_code=200)
async def update_pass(user: models.changePass):
    try:
<<<<<<< HEAD

        usrID = jwt.decode(
            user.access_token, JWT_SECRET, algorithms=[JWT_ALGORITHM]
        ).split(".")[1]
        res = db.update_pass(usrID, user.oldPass, user.newPass)
=======
        usrID = jwt.decode(user.access_token, JWT_SECRET, algorithms=[JWT_ALGORITHM])['user_id']
        res = db.update_pass(usrID,user.oldPass,user.newPass)
>>>>>>> dev

        if res:
            return {"msg": "Success"}
        else:
            return {"msg": "Wrong password"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/get_tickets_by_autor")
async def get_tickets_by_autor(id: models.onlyID):
    try:
        result = db.get_tickets_by_autor(id.id)
        if len(result) == 0:
            return result
        else:
            raise HTTPException(status_code=500, detail="No se pudo ingresar")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/login")
async def login(user: models.log_User) -> dict[str, str]:
    try:
        result = db.get_password_by_email(user.email)
        if result == user.password:
            user_id = db.get_userID_by_email(user.email)
            payload = {"user_id": user_id, "expires": time.time() + 600}
            token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
            return {"access_token": token}
        else:
            return {"access_token": "0"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/add_ticket")
async def create_ticket(ticket: models.Ticket):
    try:
        result = db.add_ticket(
            ticket.autor, ticket.contenido, ticket.categoria, ticket.prioridad
        )
        if result:
            return {"msg": "Ticket ingresado"}
        else:
            raise HTTPException(status_code=500, detail="No se puede :/")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/add_evento")
async def create_evento(evento: models.Evento):
    try:
        result = db.add_Evento(evento.ticketID, evento.contenido)
        if result:
            return {"msg": "Evento ingresado"}
        else:
            raise HTTPException(status_code=500, detail="No se puede :/")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, port=8000)
