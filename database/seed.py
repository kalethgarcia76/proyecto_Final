from app import app

from database.database import db

from models.paso_decision import PasoDecision
from models.conocimiento import Conocimiento


def cargar_arbol():

    with app.app_context():

        # -------------------------
        # ÁRBOL DE DECISIÓN
        # -------------------------

        pasos = [

            PasoDecision(
                id=1,
                categoria="General",
                pregunta="¿Cuál es el tipo principal de problema?",
                siguiente_si=2,
                siguiente_no=3
            ),

            PasoDecision(
                id=2,
                categoria="Red",
                pregunta="¿El equipo puede conectarse a la red?",
                siguiente_si=4,
                siguiente_no=5
            ),

            PasoDecision(
                id=3,
                categoria="Hardware",
                pregunta="¿El equipo enciende normalmente?",
                siguiente_si=10,
                siguiente_no=11
            ),

            PasoDecision(
                id=4,
                categoria="Internet",
                pregunta="¿Puedes abrir páginas de Internet?",
                siguiente_si=6,
                siguiente_no=7
            ),

            PasoDecision(
                id=5,
                categoria="Red",
                pregunta="¿El cable de red está conectado o el Wi-Fi está activado?",
                solucion_si=(
                    "Reinicie el adaptador de red, "
                    "verifique la dirección IP y realice "
                    "una prueba de conectividad con ping."
                ),
                solucion_no=(
                    "Conecte correctamente el cable Ethernet "
                    "o active la conexión Wi-Fi."
                )
            ),

            PasoDecision(
                id=6,
                categoria="Internet",
                pregunta="¿El problema solamente ocurre en una aplicación?",
                solucion_si=(
                    "La conectividad general funciona. "
                    "Revise la configuración de red, proxy "
                    "o permisos de la aplicación afectada."
                ),
                solucion_no=(
                    "La conexión parece funcionar correctamente. "
                    "Verifique el servicio específico que presenta "
                    "la incidencia."
                )
            ),

            PasoDecision(
                id=7,
                categoria="Internet",
                pregunta="¿El equipo tiene una dirección IP válida?",
                solucion_si=(
                    "Realice una prueba de DNS utilizando "
                    "nslookup y revise la configuración DNS."
                ),
                solucion_no=(
                    "Renueve la dirección IP mediante ipconfig /renew "
                    "y vuelva a comprobar la conectividad."
                )
            ),

            PasoDecision(
                id=10,
                categoria="Hardware",
                pregunta="¿El equipo funciona pero presenta lentitud?",
                siguiente_si=12,
                siguiente_no=13
            ),

            PasoDecision(
                id=11,
                categoria="Hardware",
                pregunta="¿El equipo muestra alguna señal de energía?",
                solucion_si=(
                    "Revise monitor, cables, almacenamiento, "
                    "memoria RAM y componentes internos."
                ),
                solucion_no=(
                    "Revise el cable de alimentación, cargador, "
                    "fuente de poder y toma eléctrica. "
                    "Si continúa sin encender, escale el incidente."
                ),
                escalar_no=True
            ),

            PasoDecision(
                id=12,
                categoria="Rendimiento",
                pregunta="¿El consumo de CPU o memoria es elevado?",
                solucion_si=(
                    "Abra el administrador de tareas, identifique "
                    "el proceso con mayor consumo y cierre únicamente "
                    "procesos no esenciales."
                ),
                solucion_no=(
                    "Revise espacio disponible en disco, programas "
                    "de inicio, actualizaciones y estado del almacenamiento."
                )
            ),

            PasoDecision(
                id=13,
                categoria="Hardware",
                pregunta="¿El problema está relacionado con un periférico?",
                solucion_si=(
                    "Verifique cables, controladores y conexión USB. "
                    "Pruebe el periférico en otro puerto."
                ),
                solucion_no=(
                    "Realice un diagnóstico general de hardware "
                    "y documente los síntomas encontrados."
                )
            ),

            PasoDecision(
                id=20,
                categoria="Impresora",
                pregunta="¿La impresora está encendida?",
                siguiente_si=21,
                siguiente_no=22
            ),

            PasoDecision(
                id=21,
                categoria="Impresora",
                pregunta="¿La impresora aparece disponible en el sistema?",
                siguiente_si=23,
                siguiente_no=24
            ),

            PasoDecision(
                id=22,
                categoria="Impresora",
                pregunta="¿La impresora recibe alimentación eléctrica?",
                solucion_si=(
                    "Verifique el botón de encendido y el estado "
                    "del panel de la impresora."
                ),
                solucion_no=(
                    "Revise cable de alimentación, toma eléctrica "
                    "y fuente de la impresora."
                )
            ),

            PasoDecision(
                id=23,
                categoria="Impresora",
                pregunta="¿El documento queda detenido en la cola de impresión?",
                solucion_si=(
                    "Abra la cola de impresión, cancele los trabajos "
                    "pendientes y reinicie el servicio de cola de impresión."
                ),
                solucion_no=(
                    "Compruebe papel, tinta/tóner, atascos y configuración "
                    "de la impresora."
                )
            ),

            PasoDecision(
                id=24,
                categoria="Impresora",
                pregunta="¿La impresora está conectada a la misma red?",
                solucion_si=(
                    "Reinstale o actualice el controlador de la impresora "
                    "y compruebe su dirección IP."
                ),
                solucion_no=(
                    "Conecte la impresora a la red correspondiente "
                    "y vuelva a agregarla al sistema."
                )
            )
        ]

        # Evitar duplicados
        for paso in pasos:

            existente = PasoDecision.query.get(
                paso.id
            )

            if not existente:

                db.session.add(paso)


        # -------------------------
        # BASE DE CONOCIMIENTO
        # -------------------------

        conocimientos = [

            Conocimiento(
                categoria="Red",
                problema="Sin conexión a Internet",
                sintomas="El equipo no puede navegar.",
                causa="Problemas de IP, DNS, adaptador o conexión.",
                procedimiento="Verificar conexión, IP, DNS y realizar pruebas de ping.",
                solucion="Restablecer la conexión y configurar correctamente los parámetros de red.",
                prioridad="Alta"
            ),

            Conocimiento(
                categoria="Wi-Fi",
                problema="Wi-Fi desconectado",
                sintomas="El equipo no detecta o no conecta a la red inalámbrica.",
                causa="Adaptador deshabilitado, señal insuficiente o configuración incorrecta.",
                procedimiento="Verificar Wi-Fi, señal, contraseña y adaptador.",
                solucion="Activar el adaptador y reconectar a la red.",
                prioridad="Media"
            ),

            Conocimiento(
                categoria="Hardware",
                problema="Equipo no enciende",
                sintomas="No inicia el sistema.",
                causa="Alimentación eléctrica o componente defectuoso.",
                procedimiento="Revisar alimentación, cargador, fuente y componentes.",
                solucion="Corregir alimentación o escalar a revisión especializada.",
                prioridad="Alta",
                requiere_escalamiento=True
            ),

            Conocimiento(
                categoria="Rendimiento",
                problema="Equipo lento",
                sintomas="Aplicaciones tardan en responder.",
                causa="Uso elevado de CPU/RAM, almacenamiento lleno o procesos innecesarios.",
                procedimiento="Revisar administrador de tareas y almacenamiento.",
                solucion="Cerrar procesos innecesarios y realizar mantenimiento.",
                prioridad="Media"
            ),

            Conocimiento(
                categoria="Impresora",
                problema="Impresora no imprime",
                sintomas="Los documentos permanecen en cola.",
                causa="Cola de impresión detenida o impresora desconectada.",
                procedimiento="Revisar cola, conexión y servicio de impresión.",
                solucion="Cancelar trabajos pendientes y reiniciar el servicio.",
                prioridad="Media"
            ),

            Conocimiento(
                categoria="Software",
                problema="Aplicación no inicia",
                sintomas="El programa se cierra o no responde.",
                causa="Archivos dañados, permisos o incompatibilidad.",
                procedimiento="Revisar permisos, actualizar y reinstalar.",
                solucion="Reparar o reinstalar la aplicación.",
                prioridad="Media"
            )
        ]

        for conocimiento in conocimientos:

            db.session.add(
                conocimiento
            )


        db.session.commit()

        print(
            "Base de conocimiento y árbol cargados correctamente."
        )


if __name__ == "__main__":

    cargar_arbol()