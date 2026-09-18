from dominio.entidades import Especie, Planta, Medicion, ValorParametro, ResultadoDiagnostico
from .dtos import MedicionRequestDTO, DiagnosticoResponseDTO, EvaluacionParametroDTO, EspecieResponseDTO


class DiagnosticoMapper:
    def a_dominio(self, dto: MedicionRequestDTO) -> Medicion:
        especie = Especie(dto.especie)
        planta = Planta(especie)

        valores = [
            ValorParametro("humedad", dto.humedad, "%"),
            ValorParametro("luz", dto.luz, "lux"),
            ValorParametro("temperatura", dto.temperatura, "C"),
        ]

        return Medicion(planta, valores)

    def a_response_dto(self, resultado: ResultadoDiagnostico) -> DiagnosticoResponseDTO:
        parametros_dto = [
            EvaluacionParametroDTO(
                nombre=p.obtener_nombre(),
                valor=p.obtener_valor(),
                unidad=p.obtener_unidad(),
                rango_optimo=(
                    p.obtener_rango_optimo().obtener_minimo(),
                    p.obtener_rango_optimo().obtener_maximo(),
                ),
                estado=p.obtener_estado().value,
            )
            for p in resultado.obtener_parametros()
        ]

        return DiagnosticoResponseDTO(
            especie=resultado.obtener_especie().obtener_nombre(),
            estado=resultado.obtener_estado().value,
            parametros=parametros_dto,
            recomendaciones=resultado.obtener_recomendaciones(),
        )

    def a_especie_response_dto(self, rango_referencia) -> EspecieResponseDTO:
        rangos_dict = {}
        for nombre, rango in rango_referencia.obtener_todos_los_rangos().items():
            rangos_dict[nombre] = {
                "min": rango.obtener_minimo(),
                "max": rango.obtener_maximo(),
            }

        return EspecieResponseDTO(
            nombre=rango_referencia.obtener_especie().obtener_nombre(),
            rangos=rangos_dict,
        )
