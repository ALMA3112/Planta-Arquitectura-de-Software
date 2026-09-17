from .excepciones import ValorParametroInvalidoError

class Especie:
    def __init__(self, nombre: str):
        if not nombre or not nombre.strip():
            raise ValueError("El nombre de la especie no puede estar vacío")
        self._nombre = nombre.strip().lower()

    def obtener_nombre(self) -> str:
        return self._nombre

    def __eq__(self, otra):
        return isinstance(otra, Especie) and self._nombre == otra._nombre

    def __repr__(self):
        return f"Especie({self._nombre})"

class RangoParametro:
    def __init__(self, minimo: float, maximo: float):
        if minimo > maximo:
            raise ValueError("El mínimo no puede ser mayor que el máximo")
        self._minimo = minimo
        self._maximo = maximo

    def contiene(self, valor: float) -> bool:
        return self._minimo <= valor <= self._maximo

    def obtener_minimo(self) -> float:
        return self._minimo

    def obtener_maximo(self) -> float:
        return self._maximo

    def __repr__(self):
        return f"RangoParametro({self._minimo}-{self._maximo})"

class ValorParametro:
    _LIMITES_FISICOS = {
        "humedad": (0, 100),
        "luz": (0, 200000),
        "temperatura": (-50, 80),
    }

    def __init__(self, nombre: str, valor: float, unidad: str):
        if not isinstance(valor, (int, float)):
            raise ValorParametroInvalidoError(nombre, "el valor debe ser numérico")

        limites = self._LIMITES_FISICOS.get(nombre)
        if limites is not None:
            minimo_fisico, maximo_fisico = limites
            if valor < minimo_fisico or valor > maximo_fisico:
                raise ValorParametroInvalidoError(
                    nombre,
                    f"el valor {valor} está fuera del rango físicamente posible "
                    f"({minimo_fisico} a {maximo_fisico})"
                )

        self._nombre = nombre
        self._valor = float(valor)
        self._unidad = unidad

    def obtener_nombre(self) -> str:
        return self._nombre

    def obtener_valor(self) -> float:
        return self._valor

    def obtener_unidad(self) -> str:
        return self._unidad

    def __repr__(self):
        return f"ValorParametro({self._nombre}={self._valor}{self._unidad})"

class EvaluacionParametro:
    def __init__(self, nombre: str, valor: float, unidad: str,
                 rango_optimo: "RangoParametro", estado):
        self._nombre = nombre
        self._valor = valor
        self._unidad = unidad
        self._rango_optimo = rango_optimo
        self._estado = estado

    def obtener_nombre(self) -> str:
        return self._nombre

    def obtener_valor(self) -> float:
        return self._valor

    def obtener_unidad(self) -> str:
        return self._unidad

    def obtener_rango_optimo(self) -> "RangoParametro":
        return self._rango_optimo

    def obtener_estado(self):
        return self._estado

    def __repr__(self):
        return f"EvaluacionParametro({self._nombre}={self._valor}{self._unidad}, estado={self._estado})"

class ResultadoDiagnostico:
    def __init__(self, especie: "Especie", estado,
                 parametros: list, recomendaciones: list):
        self._especie = especie
        self._estado = estado
        self._parametros = parametros
        self._recomendaciones = recomendaciones

    def obtener_especie(self) -> "Especie":
        return self._especie

    def obtener_estado(self):
        return self._estado

    def obtener_parametros(self) -> list:
        return self._parametros

    def obtener_recomendaciones(self) -> list:
        return self._recomendaciones

    def __repr__(self):
        return f"ResultadoDiagnostico(especie={self._especie}, estado={self._estado})"

class Planta:
    def __init__(self, especie: "Especie"):
        self._especie = especie

    def obtener_especie(self) -> "Especie":
        return self._especie

    def __repr__(self):
        return f"Planta(especie={self._especie})"

class Medicion:
    def __init__(self, planta: "Planta", valores: list):
        self._planta = planta
        self._valores = valores

    def obtener_planta(self) -> "Planta":
        return self._planta

    def obtener_valor(self, nombre: str):
        for valor in self._valores:
            if valor.obtener_nombre() == nombre:
                return valor
        return None

    def obtener_todos_los_valores(self) -> list:
        return self._valores

    def __repr__(self):
        return f"Medicion(planta={self._planta}, valores={self._valores})"

class RangoReferencia:
    def __init__(self, especie: "Especie", rangos: dict):
        self._especie = especie
        self._rangos = rangos

    def obtener_especie(self) -> "Especie":
        return self._especie

    def obtener_rango(self, nombre_parametro: str) -> "RangoParametro":
        rango = self._rangos.get(nombre_parametro)
        if rango is None:
            raise ValueError(f"No existe rango definido para el parámetro '{nombre_parametro}'")
        return rango

    def obtener_todos_los_rangos(self) -> dict:
        return self._rangos

    def __repr__(self):
        return f"RangoReferencia(especie={self._especie}, rangos={self._rangos})"


