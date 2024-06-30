from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel

from engine.entities import Solicitud, SolicitudCreate, Grimorio
from engine.use_cases import SolicitudService
from adapters.database import get_db
from adapters.repository import SolicitudRepository
from adapters.grimorio_assigner import GrimorioAssigner

router = APIRouter()

class StatusUpdate(BaseModel):
    status: str

@router.post("/solicitud", response_model=Solicitud, summary="Crear Solicitud", description="Crea una nueva solicitud de ingreso a la academia de magia.")
def create_solicitud(solicitud: SolicitudCreate, db: Session = Depends(get_db)):
    """
    Crea una nueva solicitud de ingreso a la academia de magia.

    - **nombre**: Solo letras, máximo 20 caracteres.
    - **apellido**: Solo letras, máximo 20 caracteres.
    - **identificacion**: Números y letras, máximo 10 caracteres.
    - **edad**: Solo números, 2 dígitos.
    - **afinidad_magica**: Una única opción entre Oscuridad, Luz, Fuego, Agua, Viento o Tierra.
    """
    repository = SolicitudRepository(db)
    grimorio_assigner = GrimorioAssigner()
    solicitud_service = SolicitudService(repository, grimorio_assigner)
    try:
        solicitud_creada = solicitud_service.create_solicitud(solicitud)
        return solicitud_creada
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/solicitud/{id}", response_model=Solicitud, summary="Actualizar Solicitud", description="Actualiza una solicitud de ingreso existente.")
def update_solicitud(id: int, solicitud: SolicitudCreate, db: Session = Depends(get_db)):
    """
    Actualiza una solicitud de ingreso existente.

    - **id**: ID de la solicitud a actualizar.
    - **nombre**: Solo letras, máximo 20 caracteres.
    - **apellido**: Solo letras, máximo 20 caracteres.
    - **identificacion**: Números y letras, máximo 10 caracteres.
    - **edad**: Solo números, 2 dígitos.
    - **afinidad_magica**: Una única opción entre Oscuridad, Luz, Fuego, Agua, Viento o Tierra.
    """
    repository = SolicitudRepository(db)
    grimorio_assigner = GrimorioAssigner()
    solicitud_service = SolicitudService(repository, grimorio_assigner)
    try:
        updated = solicitud_service.update_solicitud(id, solicitud)
        if updated:
            return updated
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/solicitudes", response_model=List[Solicitud], summary="Listar Solicitudes", description="Obtiene una lista de todas las solicitudes de ingreso.")
def list_solicitudes(db: Session = Depends(get_db)):
    """
    Obtiene una lista de todas las solicitudes de ingreso.

    No se requieren parámetros.
    """
    repository = SolicitudRepository(db)
    grimorio_assigner = GrimorioAssigner()
    solicitud_service = SolicitudService(repository, grimorio_assigner)
    return solicitud_service.list_solicitudes()

@router.patch("/solicitud/{id}/estatus", response_model=Solicitud, summary="Actualizar Estatus de Solicitud", description="Actualiza el estatus de una solicitud de ingreso existente.")
def update_status(id: int, status_update: StatusUpdate, db: Session = Depends(get_db)):
    """
    Actualiza el estatus de una solicitud de ingreso existente.

    - **id**: ID de la solicitud a actualizar.
    - **status**: Nuevo estatus de la solicitud, puede ser "aceptado" o "rechazado".
    """
    repository = SolicitudRepository(db)
    grimorio_assigner = GrimorioAssigner()
    solicitud_service = SolicitudService(repository, grimorio_assigner)
    try:
        updated = solicitud_service.update_status(id, status_update.status)
        if updated:
            return updated
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/asignaciones", response_model=Grimorio, summary="Asignar Grimorio", description="Asigna un grimorio aleatorio a una solicitud aprobada.")
def assign_grimorio(id: int, db: Session = Depends(get_db)):
    """
    Asigna un grimorio aleatorio a una solicitud aprobada.

    - **id**: Identificador de la solicitud a la cual asignar el grimorio.
    """
    repository = SolicitudRepository(db)
    grimorio_assigner = GrimorioAssigner()
    solicitud_service = SolicitudService(repository, grimorio_assigner)
    return solicitud_service.assign_grimorio(id)

@router.delete("/solicitud/{id}", response_model=bool, summary="Eliminar Solicitud", description="Elimina una solicitud de ingreso existente.")
def delete_solicitud(id: int, db: Session = Depends(get_db)):
    """
    Elimina una solicitud de ingreso existente.

    - **id**: Identificador de la solicitud a eliminar.
    """
    repository = SolicitudRepository(db)
    grimorio_assigner = GrimorioAssigner()
    solicitud_service = SolicitudService(repository, grimorio_assigner)
    return solicitud_service.delete_solicitud(id)
