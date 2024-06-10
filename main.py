import time

import uvicorn
from fastapi import FastAPI, Request, HTTPException
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel


from app.db.access import add_user, database_connect

app = FastAPI()


origins = [
    "http://localhost",
    "http://localhost:8080",
]


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


@app.get("/testdata")
async def read_main():
    return {"msg": "Hello World"}


@app.get("/")
async def root():
    return {"msg": "hola mi rey"}

class User(BaseModel):
    name: str
    email: str
    password: str
    rol: str

class Ticket(BaseModel):
    autor: int
    contenido: str
    categoria: str
    prioridad: int

class Evento(BaseModel):
    ticketID: int
    contenido: str

class Rol(BaseModel):
    userID: int
    rol: str

@app.post("/add_user")
async def create_user(user: User):
    try:
        result = add_user(user.name, user.email, user.password, user.rol)
        if result:
            return {"msg": "User Ingresado :)"}
        else:
            raise HTTPException(status_code=500, detail="No se pudo ingresar")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/add_ticket")
async def create_ticket(ticket: Ticket):
    try:
        result = add_ticket(ticket.autor, ticket.contenido, ticket.categoria, ticket.prioridad)
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

@app.post("/add_rol")
async def create_rol(rol: Rol):
    try:
        result = add_rol(rol.userID, rol.rol)
        if result:
            return {"msg": "Rol ingresado"}
        else:
            raise HTTPException(status_code=500, detail="No se puede :/")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



if __name__ == "__main__":
    uvicorn.run(app, port=8000)

