from dominio.entidades import Medicion, ResultadoDiagnostico
from dominio.puertos import RepositorioRangos
from dominio.servicios import ComparadorParametro, ReglaAgregacion, GeneradorRecomendaciones

class DiagnosticarPlantaCasoUso:
    def __init__(
        self,
        repositorio_rangos: RepositorioRangos,
        comparador: ComparadorParametro,
        regla_agregacion: ReglaAgregacion,
        generador_recomendaciones: GeneradorRecomendaciones,
    ):
        self._repositorio_rangos = repositorio_rangos
        self._comparador = comparador
        self._regla_agregacion = regla_agregacion
        self._generador_recomendaciones = generador_recomendaciones

    def ejecutar(self, medicion: Medicion) -> ResultadoDiagnostico:
        especie = medicion.obtener_planta().obtener_especie()
        rangos = self._repositorio_rangos.obtener_rangos(especie)

        evaluaciones = []
        for valor in medicion.obtener_todos_los_valores():
            rango = rangos.obtener_rango(valor.obtener_nombre())
            evaluaciones.append(self._comparador.comparar(valor, rango))

        estado_global = self._regla_agregacion.calcular(evaluaciones)
        recomendaciones = self._generador_recomendaciones.generar(evaluaciones)

        return ResultadoDiagnostico(
            especie=especie,
            estado=estado_global,
            parametros=evaluaciones,
            recomendaciones=recomendaciones,
        )

class ListarEspeciesCasoUso:
    def __init__(self, repositorio_rangos: RepositorioRangos):
        self._repositorio_rangos = repositorio_rangos

    def ejecutar(self) -> list:
        return self._repositorio_rangos.listar_especies()


