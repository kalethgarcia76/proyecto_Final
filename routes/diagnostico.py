from flask import Blueprint, render_template, request, redirect, url_for, abort
from models.paso_decision import PasoDecision
from services.motor_decision import MotorDecision

diagnostico_bp = Blueprint("diagnostico", __name__)

CATEGORIAS = {
    "red": {"nombre": "Red / Internet", "icono": "🌐", "descripcion": "Problemas de conexión, IP, DNS o Internet", "paso": 100},
    "wifi": {"nombre": "Wi-Fi", "icono": "📶", "descripcion": "Problemas con redes inalámbricas", "paso": 200},
    "impresora": {"nombre": "Impresora", "icono": "🖨️", "descripcion": "Problemas de impresión o conexión", "paso": 500},
    "hardware": {"nombre": "Hardware", "icono": "💻", "descripcion": "Problemas físicos o de encendido", "paso": 300},
    "rendimiento": {"nombre": "Rendimiento", "icono": "⚡", "descripcion": "Equipos lentos o con alto consumo", "paso": 400},
    "software": {"nombre": "Software", "icono": "💾", "descripcion": "Programas, aplicaciones y sistema operativo", "paso": 600},
}

@diagnostico_bp.route("/")
def iniciar():
    return render_template("diagnostico_inicio.html", categorias=CATEGORIAS)

@diagnostico_bp.route("/categoria/<categoria>")
def categoria(categoria):
    datos = CATEGORIAS.get(categoria)
    if not datos:
        abort(404)
    return redirect(url_for("diagnostico.paso", paso_id=datos["paso"]))

@diagnostico_bp.route("/paso/<int:paso_id>", methods=["GET", "POST"])
def paso(paso_id):
    paso_actual = MotorDecision.obtener_paso(paso_id)

    if request.method == "POST":
        resultado = MotorDecision.procesar_respuesta(paso_actual, request.form.get("respuesta"))
        if resultado["solucion"] or resultado["escalar"] or not resultado["siguiente"]:
            return render_template(
                "resultado.html",
                solucion=resultado["solucion"] or "No fue posible determinar una solución automática.",
                escalar=resultado["escalar"] or not resultado["solucion"],
                categoria=paso_actual.categoria,
            )
        return redirect(url_for("diagnostico.paso", paso_id=resultado["siguiente"]))

    total_pasos = PasoDecision.query.filter_by(categoria=paso_actual.categoria).count()
    completados = PasoDecision.query.filter(
        PasoDecision.categoria == paso_actual.categoria,
        PasoDecision.id <= paso_actual.id
    ).count()

    return render_template(
        "diagnostico.html",
        paso=paso_actual,
        total_pasos=max(total_pasos, 1),
        paso_numero=max(completados, 1),
    )

@diagnostico_bp.route("/resolver", methods=["POST"])
def resolver():
    paso_id = request.form.get("paso_id", type=int)
    respuesta = request.form.get("respuesta", "").lower()
    if not paso_id or respuesta not in {"si", "no"}:
        return redirect(url_for("diagnostico.iniciar"))

    paso = MotorDecision.obtener_paso(paso_id)
    resultado = MotorDecision.procesar_respuesta(paso, respuesta)
    if resultado["solucion"] or resultado["escalar"] or not resultado["siguiente"]:
        return render_template(
            "resultado.html",
            solucion=resultado["solucion"] or "No fue posible determinar una solución automática.",
            escalar=resultado["escalar"] or not resultado["solucion"],
            categoria=paso.categoria,
        )
    return redirect(url_for("diagnostico.paso", paso_id=resultado["siguiente"]))
