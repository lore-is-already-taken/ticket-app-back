import time

import uvicorn
from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware

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


if __name__ == "__main__":
    uvicorn.run(app, port=8000)
