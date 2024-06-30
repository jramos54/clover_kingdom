import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from adapters.database import Base, get_db
from engine.models import SolicitudModel, GrimorioAsignacionModel
import os
import random
import string

# Configuración de la base de datos
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}@{os.getenv('DATABASE_HOST')}/{os.getenv('DATABASE_NAME')}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependencia de la base de datos
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def random_identificacion(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def test_create_solicitud():
    identificacion = random_identificacion()
    response = client.post(
        "/api/v1/solicitud",
        json={
            "nombre": "Arioto",
            "apellido": "Ramos",
            "identificacion": identificacion,
            "edad": 18,
            "afinidad_magica": "Oscuridad"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "Arioto"
    assert data["apellido"] == "Ramos"
    assert data["identificacion"] == identificacion
    assert data["edad"] == 18
    assert data["afinidad_magica"] == "Oscuridad"
    assert data["status"] == "pendiente"

def test_update_status_to_aceptado():
    identificacion = random_identificacion()
    client.post(
        "/api/v1/solicitud",
        json={
            "nombre": "Arioto",
            "apellido": "Ramos",
            "identificacion": identificacion,
            "edad": 18,
            "afinidad_magica": "Oscuridad"
        }
    )
    response = client.patch(
        "/api/v1/solicitud/1/estatus",
        json={"status": "aceptado"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "aceptado"
    assert data["grimorio"] is not None

def test_list_solicitudes():
    identificacion = random_identificacion()
    client.post(
        "/api/v1/solicitud",
        json={
            "nombre": "Arioto",
            "apellido": "Ramos",
            "identificacion": identificacion,
            "edad": 18,
            "afinidad_magica": "Oscuridad"
        }
    )
    response = client.get("/api/v1/solicitudes")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["nombre"] == "Arioto"
    assert data[0]["apellido"] == "Ramos"
    assert data[0]["identificacion"] == identificacion
    assert data[0]["edad"] == 18
    assert data[0]["afinidad_magica"] == "Oscuridad"
    assert data[0]["status"] == "pendiente"
