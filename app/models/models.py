from pydantic import BaseModel


class User(BaseModel):
    name: str
    email: str
    password: str
    rol: str

class log_User(BaseModel):
    email: str
    password: str


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

class onlyID(BaseModel):
    id: int
