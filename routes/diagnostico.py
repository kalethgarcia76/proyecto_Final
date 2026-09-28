from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for
)

from models.paso_decision import PasoDecision

from services.motor_decision import MotorDecision


diagnostico_bp = Blueprint(
    "diagnostico",
    __name__
)


@diagnostico_bp.route("/")
def iniciar():

    primer_paso = PasoDecision.query.first()

    if not primer_paso:

        return render_template(
            "diagnostico.html",
            paso=None,
            total_pasos=0
        )

    return redirect(
        url_for(
            "diagnostico.paso",
            paso_id=primer_paso.id
        )
    )


@diagnostico_bp.route(
    "/paso/<int:paso_id>"
)
def paso(paso_id):

    paso_actual = MotorDecision.obtener_paso(
        paso_id
    )

    total_pasos = PasoDecision.query.count()

    return render_template(
        "diagnostico.html",
        paso=paso_actual,
        total_pasos=total_pasos
    )


@diagnostico_bp.route(
    "/resolver",
    methods=["POST"]
)
def resolver():

    paso_id = int(
        request.form["paso_id"]
    )

    respuesta = request.form["respuesta"]

    paso = MotorDecision.obtener_paso(
        paso_id
    )

    resultado = MotorDecision.procesar_respuesta(
        paso,
        respuesta
    )

    if resultado["solucion"]:

        return render_template(
            "resultado.html",
            solucion=resultado["solucion"],
            escalar=resultado["escalar"]
        )

    if resultado["siguiente"]:

        return redirect(
            url_for(
                "diagnostico.paso",
                paso_id=resultado["siguiente"]
            )
        )

    return render_template(
        "resultado.html",
        solucion=(
            "No se encontró una solución automática. "
            "El incidente debe ser escalado a un técnico especializado."
        ),
        escalar=True
    )