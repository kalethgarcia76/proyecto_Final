from models.paso_decision import PasoDecision

class MotorDecision:
    """Motor de inferencia basado en nodos almacenados en la base de datos."""

    @staticmethod
    def obtener_paso(paso_id):
        return PasoDecision.query.get_or_404(paso_id)

    @staticmethod
    def procesar_respuesta(paso, respuesta):
        respuesta = (respuesta or "").strip().lower()
        if respuesta not in {"si", "no"}:
            return {"siguiente": None, "solucion": "Respuesta no válida.", "escalar": True}

        if respuesta == "si":
            return {"siguiente": paso.siguiente_si, "solucion": paso.solucion_si, "escalar": bool(paso.escalar_si)}
        return {"siguiente": paso.siguiente_no, "solucion": paso.solucion_no, "escalar": bool(paso.escalar_no)}
