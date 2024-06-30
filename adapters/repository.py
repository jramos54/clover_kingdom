from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from typing import List, Optional
from engine.interfaces import SolicitudRepositoryInterface
from engine.entities import Solicitud, SolicitudCreate, Grimorio, StatusEnum
from engine.models import SolicitudModel, GrimorioAsignacionModel

class SolicitudRepository(SolicitudRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def create(self, solicitud: SolicitudCreate) -> Solicitud:
        exists = self.db.execute(
            select(SolicitudModel).filter_by(identificacion=solicitud.identificacion)
        ).scalar_one_or_none()
        
        if exists:
            raise ValueError("El registro ya existe, intente con otro.")

        db_solicitud = SolicitudModel(**solicitud.dict(), status=StatusEnum.pendiente)
        self.db.add(db_solicitud)
        try:
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            raise ValueError("Error al crear la solicitud. La identificación debe ser única.")
        
        self.db.refresh(db_solicitud)
        return Solicitud.from_orm(db_solicitud)

    def assign_grimorio(self, solicitud_id: int, grimorio: Grimorio) -> Grimorio:
        db_grimorio = GrimorioAsignacionModel(
            solicitud_id=solicitud_id,
            tipo=grimorio.tipo,
            rareza=grimorio.rareza
        )
        self.db.add(db_grimorio)
        self.db.commit()
        self.db.refresh(db_grimorio)
        return grimorio

    def update_status(self, id: int, status: StatusEnum) -> Optional[Solicitud]:
        db_solicitud = self.db.query(SolicitudModel).filter(SolicitudModel.id == id).first()
        if db_solicitud:
            db_solicitud.status = status
            self.db.commit()
            self.db.refresh(db_solicitud)
            return Solicitud.from_orm(db_solicitud)
        return None

    def update(self, id: int, solicitud: Solicitud) -> Optional[Solicitud]:
        db_solicitud = self.db.query(SolicitudModel).filter(SolicitudModel.id == id).first()
        if db_solicitud:
            for key, value in solicitud.dict(exclude_unset=True).items():
                setattr(db_solicitud, key, value)
            self.db.commit()
            self.db.refresh(db_solicitud)
            return Solicitud.from_orm(db_solicitud)
        return None

    def delete(self, id: int) -> bool:
        db_solicitud = self.db.query(SolicitudModel).filter(SolicitudModel.id == id).first()
        if db_solicitud:
            self.db.delete(db_solicitud)
            self.db.commit()
            return True
        return False

    def get(self, id: int) -> Optional[Solicitud]:
        db_solicitud = self.db.query(SolicitudModel).filter(SolicitudModel.id == id).first()
        if db_solicitud:
            return Solicitud.from_orm(db_solicitud)
        return None

    def list(self) -> List[Solicitud]:
        solicitudes = self.db.query(SolicitudModel).all()
        result = []
        for solicitud in solicitudes:
            grimorio_asignacion = self.db.query(GrimorioAsignacionModel).filter_by(solicitud_id=solicitud.id).first()
            solicitud_data = Solicitud.from_orm(solicitud)
            if grimorio_asignacion:
                solicitud_data.grimorio = Grimorio.from_orm(grimorio_asignacion)
            result.append(solicitud_data)
        return result
