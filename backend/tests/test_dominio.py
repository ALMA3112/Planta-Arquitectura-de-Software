import pytest

from dominio.entidades import Especie, RangoParametro, RangoReferencia, Planta, Medicion, ValorParametro
from dominio.puertos import RepositorioRangos
from dominio.servicios import ComparadorParametro, ReglaAgregacionPorConteo, GeneradorRecomendaciones
from dominio.enums import EstadoParametro, EstadoGlobal
from dominio.excepciones import EspecieNoSoportadaError, ValorParametroInvalidoError
from aplicacion.casos_uso import DiagnosticarPlantaCasoUso, ListarEspeciesCasoUso


class RepositorioRangosFalso(RepositorioRangos):
    """
    Doble de prueba: implementa la misma interfaz que RepositorioRangosCSV,
    pero con datos fijos en memoria, sin tocar ningún archivo.
    """

    def __init__(self):
        self._especie_sansevieria = Especie("sansevieria")
        self._rango_sansevieria = RangoReferencia(
            self._especie_sansevieria,
            {
                "humedad": RangoParametro(40, 70),
                "luz": RangoParametro(200, 1500),
                "temperatura": RangoParametro(18, 29),
            },
        )

    def obtener_rangos(self, especie: Especie) -> RangoReferencia:
        if especie.obtener_nombre() != "sansevieria":
            raise EspecieNoSoportadaError(especie.obtener_nombre())
        return self._rango_sansevieria

    def listar_especies(self) -> list:
        return [self._rango_sansevieria]

def test_comparador_clasifica_optimo_cuando_esta_en_rango():
    comparador = ComparadorParametro()
    valor = ValorParametro("humedad", 50, "%")
    rango = RangoParametro(40, 70)

    evaluacion = comparador.comparar(valor, rango)

    assert evaluacion.obtener_estado() == EstadoParametro.OPTIMO

def test_comparador_clasifica_bajo_cuando_esta_por_debajo():
    comparador = ComparadorParametro()
    valor = ValorParametro("humedad", 25, "%")
    rango = RangoParametro(40, 70)

    evaluacion = comparador.comparar(valor, rango)

    assert evaluacion.obtener_estado() == EstadoParametro.BAJO

def test_comparador_clasifica_alto_cuando_esta_por_encima():
    comparador = ComparadorParametro()
    valor = ValorParametro("humedad", 90, "%")
    rango = RangoParametro(40, 70)

    evaluacion = comparador.comparar(valor, rango)

    assert evaluacion.obtener_estado() == EstadoParametro.ALTO

def test_regla_agregacion_da_critico_con_dos_fuera_de_rango():
    comparador = ComparadorParametro()
    regla = ReglaAgregacionPorConteo()

    evaluaciones = [
        comparador.comparar(ValorParametro("humedad", 25, "%"), RangoParametro(40, 70)),
        comparador.comparar(ValorParametro("luz", 3000, "lux"), RangoParametro(200, 1500)),
        comparador.comparar(ValorParametro("temperatura", 21, "C"), RangoParametro(18, 29)),
    ]

    estado = regla.calcular(evaluaciones)

    assert estado == EstadoGlobal.CRITICO

def test_caso_uso_diagnostico_devuelve_resultado_correcto():
    caso_uso = DiagnosticarPlantaCasoUso(
        repositorio_rangos=RepositorioRangosFalso(),
        comparador=ComparadorParametro(),
        regla_agregacion=ReglaAgregacionPorConteo(),
        generador_recomendaciones=GeneradorRecomendaciones(),
    )

    planta = Planta(Especie("sansevieria"))
    medicion = Medicion(planta, [
        ValorParametro("humedad", 32.5, "%"),
        ValorParametro("luz", 850, "lux"),
        ValorParametro("temperatura", 21.0, "C"),
    ])

    resultado = caso_uso.ejecutar(medicion)

    assert resultado.obtener_estado() == EstadoGlobal.EN_RIESGO
    assert len(resultado.obtener_recomendaciones()) == 1

def test_caso_uso_lanza_error_con_especie_no_soportada():
    caso_uso = DiagnosticarPlantaCasoUso(
        repositorio_rangos=RepositorioRangosFalso(),
        comparador=ComparadorParametro(),
        regla_agregacion=ReglaAgregacionPorConteo(),
        generador_recomendaciones=GeneradorRecomendaciones(),
    )

    planta = Planta(Especie("cactus_marciano"))
    medicion = Medicion(planta, [
        ValorParametro("humedad", 32.5, "%"),
        ValorParametro("luz", 850, "lux"),
        ValorParametro("temperatura", 21.0, "C"),
    ])

    with pytest.raises(EspecieNoSoportadaError):
        caso_uso.ejecutar(medicion)

def test_valor_parametro_lanza_error_fuera_de_rango_fisico():
    with pytest.raises(ValorParametroInvalidoError):
        ValorParametro("humedad", -10, "%")
