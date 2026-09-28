from flask import Flask, session, redirect, url_for, request
from config import Config
from database.database import db
from models import Ticket, Conocimiento, PasoDecision, Usuario, RegistroAcceso
from routes.main import main_bp
from routes.diagnostico import diagnostico_bp
from routes.tickets import tickets_bp
from routes.conocimiento import conocimiento_bp
from routes.auth import auth_bp\nfrom routes.accesos import accesos_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    app.register_blueprint(auth_bp)\n    app.register_blueprint(accesos_bp, url_prefix="/accesos")
    app.register_blueprint(main_bp)
    app.register_blueprint(diagnostico_bp, url_prefix="/diagnostico")
    app.register_blueprint(tickets_bp, url_prefix="/tickets")
    app.register_blueprint(conocimiento_bp, url_prefix="/conocimiento")

    @app.before_request
    def require_login():
        public_endpoints = {"auth.login", "static"}

        if request.endpoint in public_endpoints:
            return None

        if not session.get("usuario_id"):
            return redirect(url_for("auth.login"))

        return None

    with app.app_context():
        db.create_all()

        from database.seed import cargar_datos
        cargar_datos()

        ensure_admin()

    return app


def ensure_admin():
    from werkzeug.security import generate_password_hash
    from models.usuario import Usuario

    admin = Usuario.query.filter_by(usuario="admin").first()

    if admin is None:
        admin = Usuario(
            nombre="Administrador TI",
            usuario="admin",
            correo="admin@mesaayuda.local",
            password_hash=generate_password_hash("Admin123!"),
            rol="administrador",
            activo=True
        )
        db.session.add(admin)
        db.session.commit()


app = create_app()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
