from database.database import db


class Conocimiento(db.Model):
    __tablename__ = "conocimiento"

    id = db.Column(db.Integer, primary_key=True)
    categoria = db.Column(db.String(80), nullable=False)
    problema = db.Column(db.String(150), nullable=False)
    sintomas = db.Column(db.Text)
    causa = db.Column(db.Text)
    procedimiento = db.Column(db.Text)
    solucion = db.Column(db.Text)
