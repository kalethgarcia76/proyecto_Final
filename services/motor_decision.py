from models.paso_decision import PasoDecision


class MotorDecision:

    @staticmethod
    def obtener_paso(paso_id):

        return PasoDecision.query.get_or_404(
            paso_id
        )

    @staticmethod
    def procesar_respuesta(paso, respuesta):

        if respuesta == "si":

            return {
                "siguiente": paso.siguiente_si,
                "solucion": paso.solucion_si,
                "escalar": paso.escalar_si
            }

        return {
            "siguiente": paso.siguiente_no,
            "solucion": paso.solucion_no,
            "escalar": paso.escalar_no
        }