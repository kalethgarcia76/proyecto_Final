from flask import Blueprint, render_template, request, redirect, url_for
from models.paso_decision import PasoDecision

diagnostico_bp = Blueprint("diagnostico", __name__)


@diagnostico_bp.route("/")
def iniciar():
    return render_template("diagnostico.html", paso=None)


@diagnostico_bp.route("/paso/<int:paso_id>")
def paso(paso_id):
    actual = PasoDecision.query.get_or_404(paso_id)
    return render_template("diagnostico.html", paso=actual)


@diagnostico_bp.route("/resolver", methods=["POST"])
def resolver():
    paso_id = int(request.form["paso_id"])
    respuesta = request.form["respuesta"]
    actual = PasoDecision.query.get_or_404(paso_id)

    siguiente = actual.siguiente_si if respuesta == "si" else actual.siguiente_no
    solucion = actual.solucion_si if respuesta == "si" else actual.solucion_no

    if solucion:
        return render_template("resultado.html", solucion=solucion)
    return redirect(url_for("diagnostico.paso", paso_id=siguiente))
