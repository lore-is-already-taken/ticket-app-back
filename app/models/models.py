from pydantic import BaseModel


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
