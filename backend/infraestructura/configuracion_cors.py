from flask_cors import CORS

class ConfiguracionCORS:
    def configurar(self, app):
        CORS(app)
