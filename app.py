from flask import Flask

from config import Config
from database.database import db

# Importar modelos para que SQLAlchemy conozca las tablas
from models.ticket import Ticket
from models.conocimiento import Conocimiento
from models.paso_decision import PasoDecision


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.route("/")
    def inicio():

        return """
        <h1>Mesa de Ayuda y Soporte TI</h1>

        <p>Sistema funcionando correctamente.</p>

        <h2>Módulos</h2>

        <ul>
            <li>Gestión de Tickets</li>
            <li>Base de Conocimiento</li>
            <li>Árbol de Decisión</li>
            <li>Diagnóstico de Incidencias</li>
        </ul>
        """

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)