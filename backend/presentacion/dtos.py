class MedicionRequestDTO:
    def __init__(self, especie: str, humedad, luz, temperatura):
        self.especie = especie
        self.humedad = humedad
        self.luz = luz
        self.temperatura = temperatura

    @staticmethod
    def desde_json(datos: dict) -> "MedicionRequestDTO":
        campos_requeridos = ["especie", "humedad", "luz", "temperatura"]
        faltantes = [c for c in campos_requeridos if c not in datos]
        if faltantes:
            raise ValueError(f"Faltan los campos: {', '.join(faltantes)}")

        return MedicionRequestDTO(
            especie=datos["especie"],
            humedad=datos["humedad"],
            luz=datos["luz"],
            temperatura=datos["temperatura"],
        )


class EvaluacionParametroDTO:
    def __init__(self, nombre, valor, unidad, rango_optimo, estado):
        self.nombre = nombre
        self.valor = valor
        self.unidad = unidad
        self.rango_optimo = rango_optimo
        self.estado = estado

    def a_dict(self) -> dict:
        return {
            "nombre": self.nombre,
            "valor": self.valor,
            "unidad": self.unidad,
            "rangoOptimo": list(self.rango_optimo),
            "estado": self.estado,
        }


class DiagnosticoResponseDTO:
    def __init__(self, especie, estado, parametros, recomendaciones):
        self.especie = especie
        self.estado = estado
        self.parametros = parametros
        self.recomendaciones = recomendaciones

    def a_dict(self) -> dict:
        return {
            "especie": self.especie,
            "estado": self.estado,
            "parametros": [p.a_dict() for p in self.parametros],
            "recomendaciones": self.recomendaciones,
        }


class EspecieResponseDTO:
    def __init__(self, nombre, rangos):
        self.nombre = nombre
        self.rangos = rangos

    def a_dict(self) -> dict:
        return {
            "nombre": self.nombre,
            "rangos": self.rangos,
        }


class ErrorResponseDTO:
    def __init__(self, error, mensaje, detalle):
        self.error = error
        self.mensaje = mensaje
        self.detalle = detalle

    def a_dict(self) -> dict:
        return {
            "error": self.error,
            "mensaje": self.mensaje,
            "detalle": self.detalle,
        }
