from abc import ABC, abstractmethod
from .entidades import Especie, RangoReferencia

class RepositorioRangos(ABC):

    @abstractmethod
    def obtener_rangos(self, especie: Especie) -> RangoReferencia:
        ...

    @abstractmethod
    def listar_especies(self) -> list:
        ...
