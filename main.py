from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {"message": "HelloWorld!"}


@app.get("/helloworld")
def saludo():
    return "Saludos waxo"
