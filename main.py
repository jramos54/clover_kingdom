# main.py
import os
from fastapi import FastAPI
from routers import solicitud
from adapters.database import engine, Base
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

app = FastAPI(
    title="Clover Kingdom Magic Academy API",
    description="API para gestionar las solicitudes de ingreso y la asignación de grimorios en la academia de magia del Reino del Trébol.",
    version="1.0.0"
)

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

app.include_router(solicitud.router, prefix="/api/v1")

@app.get("/", summary="Root", description="Endpoint raíz de la API.")
def read_root():
    """
    Endpoint raíz de la API.

    Devuelve un mensaje de bienvenida.
    """
    return {"message": "Welcome to Clover Kingdom Magic Academy API"}
