from flask import Flask, render_template
from config import Config
from database.database import db
from routes.main import main_bp
from routes.diagnostico import diagnostico_bp
from routes.tickets import tickets_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    app.register_blueprint(main_bp)
    app.register_blueprint(diagnostico_bp, url_prefix="/diagnostico")
    app.register_blueprint(tickets_bp, url_prefix="/tickets")

    with app.app_context():
        db.create_all()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
