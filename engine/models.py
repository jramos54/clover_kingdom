from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from adapters.database import engine

from sqlalchemy.orm import relationship
from adapters.database import Base
import enum

class StatusEnum(enum.Enum):
    pendiente = "pendiente"
    aceptado = "aceptado"
    rechazado = "rechazado"

class SolicitudModel(Base):
    __tablename__ = "solicitudes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(20), index=True)
    apellido = Column(String(20), index=True)
    identificacion = Column(String(10), unique=True, index=True)
    edad = Column(Integer)
    afinidad_magica = Column(String(20))
    status = Column(Enum(StatusEnum), default=StatusEnum.pendiente, nullable=False)
    
    grimorio = relationship("GrimorioAsignacionModel", back_populates="solicitud", uselist=False)

class GrimorioAsignacionModel(Base):
    __tablename__ = "grimorio_asignaciones"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    solicitud_id = Column(Integer, ForeignKey("solicitudes.id"))
    tipo = Column(String(50))
    rareza = Column(Integer)
    
    solicitud = relationship("SolicitudModel", back_populates="grimorio")

# Crear las tablas
Base.metadata.create_all(bind=engine)
