from dominio.excepciones import EspecieNoSoportadaError, ValorParametroInvalidoError
from .dtos import ErrorResponseDTO


class ManejadorErrores:
    def manejar_especie_no_soportada(self, error: EspecieNoSoportadaError) -> ErrorResponseDTO:
        return ErrorResponseDTO(
            error="ESPECIE_NO_SOPORTADA",
            mensaje=f"La especie '{error.especie}' no está soportada",
            detalle={"especie": error.especie},
        )

    def manejar_valor_invalido(self, error: ValorParametroInvalidoError) -> ErrorResponseDTO:
        return ErrorResponseDTO(
            error="PARAMETRO_INVALIDO",
            mensaje=str(error),
            detalle={"campo": error.nombre_parametro},
        )

    def manejar_campo_faltante(self, error: ValueError) -> ErrorResponseDTO:
        return ErrorResponseDTO(
            error="PARAMETRO_INVALIDO",
            mensaje=str(error),
            detalle={"campo": "desconocido"},
        )
