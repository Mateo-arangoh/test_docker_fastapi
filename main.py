from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def inicio():
    return {"mensaje": "Aplicacion FastAPI funcionando en AWS EC2"}

@app.get("/saludo")
def saludo():
    return {"mensaje": "Hola desde FastAPI"}