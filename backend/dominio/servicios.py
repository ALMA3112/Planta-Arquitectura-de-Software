from abc import ABC, abstractmethod
from .entidades import ValorParametro, RangoParametro, EvaluacionParametro
from .enums import EstadoParametro, EstadoGlobal

class ComparadorParametro:
    def comparar(self, valor: ValorParametro, rango: RangoParametro) -> EvaluacionParametro:
        if rango.contiene(valor.obtener_valor()):
            estado = EstadoParametro.OPTIMO
        elif valor.obtener_valor() < rango.obtener_minimo():
            estado = EstadoParametro.BAJO
        else:
            estado = EstadoParametro.ALTO

        return EvaluacionParametro(
            nombre=valor.obtener_nombre(),
            valor=valor.obtener_valor(),
            unidad=valor.obtener_unidad(),
            rango_optimo=rango,
            estado=estado,
        )

class ReglaAgregacion(ABC):
    @abstractmethod
    def calcular(self, evaluaciones: list) -> EstadoGlobal:
        ...

class ReglaAgregacionPorConteo(ReglaAgregacion):
    def calcular(self, evaluaciones: list) -> EstadoGlobal:
        fuera_de_rango = sum(
            1 for e in evaluaciones if e.obtener_estado() != EstadoParametro.OPTIMO
        )

        if fuera_de_rango >= 2:
            return EstadoGlobal.CRITICO
        if fuera_de_rango == 1:
            return EstadoGlobal.EN_RIESGO
        return EstadoGlobal.SALUDABLE

class GeneradorRecomendaciones:
    def generar(self, evaluaciones: list) -> list:
        recomendaciones = []
        for e in evaluaciones:
            if e.obtener_estado() == EstadoParametro.OPTIMO:
                continue

            rango = e.obtener_rango_optimo()
            if e.obtener_estado() == EstadoParametro.BAJO:
                mensaje = (
                    f"{e.obtener_nombre().capitalize()} está por debajo del rango "
                    f"recomendado ({rango.obtener_minimo()}-{rango.obtener_maximo()} {e.obtener_unidad()})."
                )
            else:
                mensaje = (
                    f"{e.obtener_nombre().capitalize()} está por encima del rango "
                    f"recomendado ({rango.obtener_minimo()}-{rango.obtener_maximo()} {e.obtener_unidad()})."
                )
            recomendaciones.append(mensaje)

        return recomendaciones

