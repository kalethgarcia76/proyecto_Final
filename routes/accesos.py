from flask import Blueprint, render_template, session, redirect, url_for, abort

from models.usuario import RegistroAcceso


accesos_bp = Blueprint("accesos", __name__)


@accesos_bp.route("/")
def listar():
    if session.get("rol") != "administrador":
        abort(403)

    registros = RegistroAcceso.query.order_by(
        RegistroAcceso.fecha_hora.desc()
    ).limit(200).all()

    return render_template(
        "accesos.html",
        registros=registros
    )
