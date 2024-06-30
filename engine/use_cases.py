from typing import Optional, List
from .interfaces import SolicitudRepositoryInterface, GrimorioAssignerInterface
from .entities import Solicitud, Grimorio, SolicitudCreate,StatusEnum

class SolicitudService:
    def __init__(self, repository: SolicitudRepositoryInterface, grimorio_assigner: GrimorioAssignerInterface):
        self.repository = repository
        self.grimorio_assigner = grimorio_assigner

    def create_solicitud(self, solicitud: SolicitudCreate) -> Solicitud:
        return self.repository.create(solicitud)

    def update_solicitud(self, id: int, solicitud: Solicitud) -> Optional[Solicitud]:
        return self.repository.update(id, solicitud)

    def delete_solicitud(self, id: int) -> bool:
        return self.repository.delete(id)

    def list_solicitudes(self) -> List[Solicitud]:
        return self.repository.list()

    def assign_grimorio(self, id: int) -> Grimorio:
        solicitud = self.repository.get(id)
        if solicitud:
            grimorio = self.grimorio_assigner.assign_grimorio(solicitud)
            self.repository.assign_grimorio(id, grimorio)
            return grimorio
        raise ValueError("Solicitud no encontrada")
    
    def update_status(self, id: int, status: StatusEnum) -> Optional[Solicitud]:
        solicitud_actualizada = self.repository.update_status(id, status)
        if solicitud_actualizada and status == StatusEnum.aceptado:
            grimorio = self.grimorio_assigner.assign_grimorio(solicitud_actualizada)
            self.repository.assign_grimorio(solicitud_actualizada.id, grimorio)
        return solicitud_actualizada
