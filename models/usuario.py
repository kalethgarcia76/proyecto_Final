from datetime import datetime
from database.database import db


class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)

    nombre = db.Column(db.String(100), nullable=False)

    usuario = db.Column(
        db.String(50),
        unique=True,
        nullable=False,
        index=True
    )

    correo = db.Column(
        db.String(150),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    rol = db.Column(
        db.String(40),
        nullable=False,
        default="tecnico"
    )

    activo = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )

    creado_en = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    ultimo_acceso = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f"<Usuario {self.usuario}>"


class RegistroAcceso(db.Model):
    __tablename__ = "registros_acceso"

    id = db.Column(db.Integer, primary_key=True)

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        nullable=True
    )

    usuario = db.Column(db.String(50), nullable=False)

    fecha_hora = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    ip = db.Column(
        db.String(64),
        nullable=True
    )

    exitoso = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )

    motivo = db.Column(
        db.String(255),
        nullable=True
    )

    usuario_relacion = db.relationship(
        "Usuario",
        backref=db.backref("registros_acceso", lazy=True)
    )

    def __repr__(self):
        return f"<RegistroAcceso {self.usuario} {self.fecha_hora}>"
