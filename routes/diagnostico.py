from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for
)

from models.paso_decision import PasoDecision


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
            paso=None
        )

    return redirect(
        url_for(
            "diagnostico.paso",
            paso_id=primer_paso.id
        )
    )


@diagnostico_bp.route("/paso/<int:paso_id>")
def paso(paso_id):

    paso_actual = PasoDecision.query.get_or_404(
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

    paso_actual = PasoDecision.query.get_or_404(
        paso_id
    )

    if respuesta == "si":

        siguiente = paso_actual.siguiente_si
        solucion = paso_actual.solucion_si
        escalar = paso_actual.escalar_si

    else:

        siguiente = paso_actual.siguiente_no
        solucion = paso_actual.solucion_no
        escalar = paso_actual.escalar_no

    # Si encontramos una solución
    if solucion:

        return render_template(
            "resultado.html",
            solucion=solucion,
            escalar=escalar
        )

    # Continuar con el siguiente nodo
    if siguiente:

        return redirect(
            url_for(
                "diagnostico.paso",
                paso_id=siguiente
            )
        )

    return render_template(
        "resultado.html",
        solucion="No se encontró una solución automática. El incidente debe ser revisado por un técnico especializado.",
        escalar=True
    )