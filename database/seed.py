from app import app
from database.database import db

from models.paso_decision import PasoDecision


def cargar_datos():

    with app.app_context():

        if PasoDecision.query.first():

            print("Los datos ya existen.")

            return


        pasos = [

            PasoDecision(
                id=1,
                categoria="Red",
                pregunta="¿El equipo tiene conexión a Internet?",
                siguiente_si=2,
                siguiente_no=3
            ),

            PasoDecision(
                id=2,
                categoria="Red",
                pregunta="¿Puedes abrir páginas web?",
                solucion_si="La conexión de red funciona correctamente. Verifique el servicio o aplicación que presenta el problema.",
                solucion_no="Revise la configuración DNS y realice una prueba de conectividad mediante ping."
            ),

            PasoDecision(
                id=3,
                categoria="Red",
                pregunta="¿El equipo está conectado al router mediante cable o Wi-Fi?",
                solucion_si="Verifique la dirección IP del equipo y reinicie la conexión de red.",
                solucion_no="Conecte el equipo a la red mediante cable Ethernet o Wi-Fi."
            )

        ]


        db.session.add_all(pasos)

        db.session.commit()


        print(
            "Árbol de decisión inicial cargado correctamente."
        )


if __name__ == "__main__":

    cargar_datos()