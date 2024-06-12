import time

import jwt
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from starlette.middleware.cors import CORSMiddleware

from app.db.access import (
    add_Evento,
    add_rol,
    add_ticket,
    add_user,
    database_connect,
    get_all_tickets,
    get_password_by_email,
    get_userID_by_email,
)
from app.models.models import Evento, Ticket, User, log_User

app = FastAPI()


origins = [
    "http://localhost",
    "http://localhost:8080",
]


JWT_SECRET = "please_please_update_me_please"
JWT_ALGORITHM = "HS256"


# app.add_middleware(HTTPSRedirectMiddleware)
conn = database_connect()
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
async def create_user(user: User):
    try:
        result = add_user(user.name, user.email, user.password, user.rol)
        if result:
            usr = log_User()
            usr.email = user.email
            usr.password = user.password
            return login(usr)
        else:
            raise HTTPException(status_code=500, detail="No se pudo ingresar")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/get_tickets")
async def get_tickets():
    try:
        result = get_all_tickets()
        if result:
            return result
        else:
            raise HTTPException(status_code=500, detail="No se pudo ingresar")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/login")
async def login(user: log_User):
    try:
        result = get_password_by_email(user.email)
        if result == user.password:
            user_id = get_userID_by_email(user.email)
            payload = {"user_id": user_id, "expires": time.time() + 600}
            token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
            return {"access_token": token}
        else:
            return {"msg": "False"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/add_ticket")
async def create_ticket(ticket: Ticket):
    try:
        result = add_ticket(
            ticket.autor, ticket.contenido, ticket.categoria, ticket.prioridad
        )
        if result:
            return {"msg": "Ticket ingresado"}
        else:
            raise HTTPException(status_code=500, detail="No se puede :/")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/add_evento")
async def create_evento(evento: Evento):
    try:
        result = add_Evento(evento.ticketID, evento.contenido)
        if result:
            return {"msg": "Evento ingresado"}
        else:
            raise HTTPException(status_code=500, detail="No se puede :/")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, port=8000)
