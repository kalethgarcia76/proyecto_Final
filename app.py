from flask import Flask

from config import Config

from database.database import db

from models import (
    Ticket,
    Conocimiento,
    PasoDecision
)

from routes.main import main_bp
from routes.diagnostico import diagnostico_bp
from routes.tickets import tickets_bp
from routes.conocimiento import conocimiento_bp


def create_app():

    app = Flask(__name__)

    app.config.from_object(
        Config
    )

    db.init_app(app)

    app.register_blueprint(
        main_bp
    )

    app.register_blueprint(
        diagnostico_bp,
        url_prefix="/diagnostico"
    )

    app.register_blueprint(
        tickets_bp,
        url_prefix="/tickets"
    )

    app.register_blueprint(
        conocimiento_bp,
        url_prefix="/conocimiento"
    )

    with app.app_context():

        db.create_all()

    return app


app = create_app()


if __name__ == "__main__":

    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )