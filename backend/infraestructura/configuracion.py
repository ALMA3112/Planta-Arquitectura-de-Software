import os

from infraestructura.repositorio_csv import RepositorioRangosCSV
from aplicacion.casos_uso import DiagnosticarPlantaCasoUso, ListarEspeciesCasoUso
from dominio.servicios import ComparadorParametro, ReglaAgregacionPorConteo, GeneradorRecomendaciones

class ConfiguracionAplicacion:
    def __init__(self):
        ruta_base = os.path.dirname(os.path.abspath(__file__))
        self._ruta_csv = os.path.join(ruta_base, "datos", "especies.csv")

    def crear_repositorio_rangos(self) -> RepositorioRangosCSV:
        return RepositorioRangosCSV(self._ruta_csv)

    def crear_caso_uso_diagnostico(self) -> DiagnosticarPlantaCasoUso:
        return DiagnosticarPlantaCasoUso(
            repositorio_rangos=self.crear_repositorio_rangos(),
            comparador=ComparadorParametro(),
            regla_agregacion=ReglaAgregacionPorConteo(),
            generador_recomendaciones=GeneradorRecomendaciones(),
        )

    def crear_caso_uso_listar_especies(self) -> ListarEspeciesCasoUso:
        return ListarEspeciesCasoUso(
            repositorio_rangos=self.crear_repositorio_rangos()
        )
