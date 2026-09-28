from datetime import datetime
from database.database import db


class Ticket(db.Model):
    __tablename__ = "tickets"

    id = db.Column(db.Integer, primary_key=True)

    codigo = db.Column(
        db.String(30),
        unique=True,
        nullable=False
    )

    titulo = db.Column(
        db.String(150),
        nullable=False
    )

    categoria = db.Column(
        db.String(80),
        nullable=False
    )

    prioridad = db.Column(
        db.String(30),
        default="Media"
    )

    estado = db.Column(
        db.String(40),
        default="Nuevo"
    )

    descripcion = db.Column(
        db.Text,
        nullable=False
    )

    diagnostico = db.Column(
        db.Text
    )

    solucion = db.Column(
        db.Text
    )

    tecnico = db.Column(
        db.String(100)
    )

    creado_en = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    actualizado_en = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )