from flask import Flask

from infraestructura.configuracion import ConfiguracionAplicacion
from infraestructura.configuracion_cors import ConfiguracionCORS
from presentacion.controller import DiagnosticoController


def crear_app():
    app = Flask(__name__)

    ConfiguracionCORS().configurar(app)

    configuracion = ConfiguracionAplicacion()
    controller = DiagnosticoController(
        caso_uso_diagnostico=configuracion.crear_caso_uso_diagnostico(),
        caso_uso_listar_especies=configuracion.crear_caso_uso_listar_especies(),
    )

    app.add_url_rule(
        "/api/v1/diagnosticos", view_func=controller.diagnosticar, methods=["POST"]
    )
    app.add_url_rule(
        "/api/v1/especies", view_func=controller.listar_especies, methods=["GET"]
    )

    return app


if __name__ == "__main__":
    app = crear_app()
    app.run(debug=True, port=5000)
