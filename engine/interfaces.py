from abc import ABC, abstractmethod
from typing import List, Optional
from .entities import Solicitud, Grimorio

class SolicitudRepositoryInterface(ABC):
    @abstractmethod
    def create(self, solicitud: Solicitud) -> Solicitud:
        pass

    @abstractmethod
    def update(self, id: int, solicitud: Solicitud) -> Optional[Solicitud]:
        pass

    @abstractmethod
    def delete(self, id: int) -> bool:
        pass

    @abstractmethod
    def get(self, id: int) -> Optional[Solicitud]:
        pass

    @abstractmethod
    def list(self) -> List[Solicitud]:
        pass

class GrimorioAssignerInterface(ABC):
    @abstractmethod
    def assign_grimorio(self, solicitud: Solicitud) -> Grimorio:
        pass