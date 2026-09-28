from database.database import db


class PasoDecision(db.Model):
    __tablename__ = "pasos_decision"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    categoria = db.Column(
        db.String(80),
        nullable=False
    )

    pregunta = db.Column(
        db.String(250),
        nullable=False
    )

    opcion_si = db.Column(
        db.String(250)
    )

    opcion_no = db.Column(
        db.String(250)
    )

    siguiente_si = db.Column(
        db.Integer
    )

    siguiente_no = db.Column(
        db.Integer
    )

    solucion_si = db.Column(
        db.Text
    )

    solucion_no = db.Column(
        db.Text
    )

    escalamiento = db.Column(
        db.Boolean,
        default=False
    )

    def __repr__(self):
        return f"<PasoDecision {self.id}>"