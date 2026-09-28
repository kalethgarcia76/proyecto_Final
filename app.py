from flask import Flask

from config import Config
from database.database import db

from models import Ticket, Conocimiento, PasoDecision

from routes.main import main_bp
from routes.diagnostico import diagnostico_bp


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    # Registrar rutas
    app.register_blueprint(main_bp)
    app.register_blueprint(
        diagnostico_bp,
        url_prefix="/diagnostico"
    )

    # Crear tablas
    with app.app_context():
        db.create_all()

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)