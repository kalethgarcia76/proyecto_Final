from flask import Blueprint, render_template

from models.conocimiento import Conocimiento


conocimiento_bp = Blueprint(
    "conocimiento",
    __name__
)


@conocimiento_bp.route("/")
def listar():

    conocimientos = Conocimiento.query.order_by(
        Conocimiento.categoria
    ).all()

    return render_template(
        "conocimiento.html",
        conocimientos=conocimientos
    )