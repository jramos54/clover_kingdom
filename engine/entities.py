from pydantic import BaseModel, Field, field_validator
from typing import Optional
from enum import Enum

class StatusEnum(str, Enum):
    pendiente = "pendiente"
    aceptado = "aceptado"
    rechazado = "rechazado"

class Grimorio(BaseModel):
    tipo: str
    rareza: int

    model_config = {
        "from_attributes": True
    }

class SolicitudBase(BaseModel):
    nombre: str = Field(..., max_length=20, pattern="^[a-zA-Z]+$")
    apellido: str = Field(..., max_length=20, pattern="^[a-zA-Z]+$")
    identificacion: str = Field(..., max_length=10, pattern="^[a-zA-Z0-9]+$")
    edad: int = Field(..., ge=10, le=99)
    afinidad_magica: str

    @field_validator('afinidad_magica')
    def check_afinidad(cls, v):
        if v not in ['Oscuridad', 'Luz', 'Fuego', 'Agua', 'Viento', 'Tierra']:
            raise ValueError('Afinidad mágica inválida')
        return v

class SolicitudCreate(SolicitudBase):
    pass

class Solicitud(SolicitudBase):
    id: int
    status: StatusEnum
    grimorio: Optional[Grimorio] = None

    model_config = {
        "from_attributes": True
    }

class StatusUpdate(BaseModel):
    status: StatusEnum