import csv
import os

from dominio.puertos import RepositorioRangos
from dominio.entidades import Especie, RangoParametro, RangoReferencia
from dominio.excepciones import EspecieNoSoportadaError

class RepositorioRangosCSV(RepositorioRangos):
    def __init__(self, ruta_archivo: str):
        self._ruta_archivo = ruta_archivo
        self._cache = None

    def obtener_rangos(self, especie: Especie) -> RangoReferencia:
        rangos_por_especie = self._leer_archivo()
        nombre_buscado = especie.obtener_nombre()

        if nombre_buscado not in rangos_por_especie:
            raise EspecieNoSoportadaError(nombre_buscado)

        return rangos_por_especie[nombre_buscado]

    def listar_especies(self) -> list:
        rangos_por_especie = self._leer_archivo()
        return list(rangos_por_especie.values())

    def _leer_archivo(self) -> dict:
        if self._cache is not None:
            return self._cache

        if not os.path.exists(self._ruta_archivo):
            raise FileNotFoundError(f"No se encontró el archivo de especies: {self._ruta_archivo}")

        resultado = {}
        with open(self._ruta_archivo, newline="", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                nombre_especie = fila["especie"].strip().lower()
                especie = Especie(nombre_especie)

                rangos = {
                    "humedad": RangoParametro(
                        float(fila["humedad_min"]), float(fila["humedad_max"])
                    ),
                    "luz": RangoParametro(
                        float(fila["luz_min"]), float(fila["luz_max"])
                    ),
                    "temperatura": RangoParametro(
                        float(fila["temp_min"]), float(fila["temp_max"])
                    ),
                }

                resultado[nombre_especie] = RangoReferencia(especie, rangos)

        self._cache = resultado
        return resultado

