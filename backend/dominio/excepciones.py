class EspecieNoSoportadaError(Exception):
    def __init__(self, especie: str):
        self.especie = especie
        super().__init__(f"La especie '{especie}' no está soportada")

class ValorParametroInvalidoError(Exception):
    def __init__(self, nombre_parametro: str, motivo: str):
        self.nombre_parametro = nombre_parametro
        self.motivo = motivo
        super().__init__(f"Valor inválido para '{nombre_parametro}': {motivo}")
