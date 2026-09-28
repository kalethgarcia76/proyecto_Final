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


# Categorías disponibles
CATEGORIAS = {
    "red": {
        "nombre": "Red / Internet",
        "icono": "🌐",
        "descripcion": "Problemas de conexión, IP, DNS o Internet",
        "paso": 2
    },

    "wifi": {
        "nombre": "Wi-Fi",
        "icono": "📶",
        "descripcion": "Problemas con redes inalámbricas",
        "paso": 2
    },

    "impresora": {
        "nombre": "Impresora",
        "icono": "🖨️",
        "descripcion": "Problemas de impresión o conexión",
        "paso": 20
    },

    "hardware": {
        "nombre": "Hardware",
        "icono": "💻",
        "descripcion": "Problemas físicos del equipo",
        "paso": 3
    },

    "rendimiento": {
        "nombre": "Rendimiento",
        "icono": "🐌",
        "descripcion": "Equipos lentos o con alto consumo",
        "paso": 10
    },

    "software": {
        "nombre": "Software",
        "icono": "💾",
        "descripcion": "Programas, aplicaciones y sistema operativo",
        "paso": 30
    }
}


@diagnostico_bp.route("/")
def iniciar():

    return render_template(
        "diagnostico_inicio.html",
        categorias=CATEGORIAS
    )


@diagnostico_bp.route(
    "/categoria/<categoria>"
)
def categoria(categoria):

    if categoria not in CATEGORIAS:

        return redirect(
            url_for(
                "diagnostico.iniciar"
            )
        )

    paso_id = CATEGORIAS[categoria]["paso"]

    return redirect(
        url_for(
            "diagnostico.paso",
            paso_id=paso_id
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

    # Si encontramos una solución
    if resultado["solucion"]:

        return render_template(
            "resultado.html",
            solucion=resultado["solucion"],
            escalar=resultado["escalar"]
        )

    # Si debemos continuar
    if resultado["siguiente"]:

        return redirect(
            url_for(
                "diagnostico.paso",
                paso_id=resultado["siguiente"]
            )
        )

    # Si no hay solución
    return render_template(
        "resultado.html",
        solucion=(
            "No fue posible determinar una solución "
            "automática. El incidente debe ser revisado "
            "por un técnico especializado."
        ),
        escalar=True
    )