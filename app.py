from flask import Flask

from config import Config
from database.database import db


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
        """

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)