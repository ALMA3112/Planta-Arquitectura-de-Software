from flask import Flask, request, jsonify

from aplicacion.casos_uso import DiagnosticarPlantaCasoUso, ListarEspeciesCasoUso
from dominio.excepciones import EspecieNoSoportadaError, ValorParametroInvalidoError
from .dtos import MedicionRequestDTO
from .mapper import DiagnosticoMapper
from .manejador_errores import ManejadorErrores

class DiagnosticoController:
    def __init__(
        self,
        caso_uso_diagnostico: DiagnosticarPlantaCasoUso,
        caso_uso_listar_especies: ListarEspeciesCasoUso,
    ):
        self._caso_uso_diagnostico = caso_uso_diagnostico
        self._caso_uso_listar_especies = caso_uso_listar_especies
        self._mapper = DiagnosticoMapper()
        self._manejador_errores = ManejadorErrores()

    def diagnosticar(self):
        try:
            dto_entrada = MedicionRequestDTO.desde_json(request.get_json(force=True))
            medicion = self._mapper.a_dominio(dto_entrada)
            resultado = self._caso_uso_diagnostico.ejecutar(medicion)
            dto_salida = self._mapper.a_response_dto(resultado)
            return jsonify(dto_salida.a_dict()), 200

        except EspecieNoSoportadaError as error:
            error_dto = self._manejador_errores.manejar_especie_no_soportada(error)
            return jsonify(error_dto.a_dict()), 404

        except ValorParametroInvalidoError as error:
            error_dto = self._manejador_errores.manejar_valor_invalido(error)
            return jsonify(error_dto.a_dict()), 400

        except ValueError as error:
            error_dto = self._manejador_errores.manejar_campo_faltante(error)
            return jsonify(error_dto.a_dict()), 400

    def listar_especies(self):
        rangos = self._caso_uso_listar_especies.ejecutar()
        dtos = [self._mapper.a_especie_response_dto(r) for r in rangos]
        return jsonify([dto.a_dict() for dto in dtos]), 200
