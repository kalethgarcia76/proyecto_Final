from database.database import db
from models.paso_decision import PasoDecision
from models.conocimiento import Conocimiento

def cargar_datos():
    pasos = [
        (100,"Red","¿El equipo está conectado a la red?",None,"Conecte el cable Ethernet o active el adaptador de red.",101,None,None,False,False),
        (101,"Red","¿El equipo tiene una dirección IP válida?",None,"Renueve la dirección IP con ipconfig /renew.",102,None,None,False,False),
        (102,"Red","¿Puede hacer ping al gateway?",None,"Revise conexión con router, cableado, VLAN y adaptador.",103,None,None,False,True),
        (103,"Red","¿Puede navegar por Internet?","La conectividad funciona; revise la aplicación específica si persiste el incidente.","Pruebe DNS con nslookup y revise los servidores DNS.",None,None,None,False,True),
        (200,"Wi-Fi","¿El Wi-Fi está activado?",None,"Active el adaptador Wi-Fi.",201,None,None,False,False),
        (201,"Wi-Fi","¿La red inalámbrica aparece disponible?",None,"Revise señal y punto de acceso.",202,None,None,False,False),
        (202,"Wi-Fi","¿La contraseña permite conectarse?",None,"Olvide la red y vuelva a conectarse con la contraseña correcta.",203,None,None,False,False),
        (203,"Wi-Fi","¿El equipo obtiene una dirección IP?","La conexión Wi-Fi está establecida; si no hay Internet, revise DNS/red.","Renueve DHCP y revise el router o servidor DHCP.",None,None,None,False,True),
        (300,"Hardware","¿El equipo enciende normalmente?",None,"Revise alimentación, cargador/fuente, toma y cableado. Si continúa, escale.",301,None,None,False,True),
        (301,"Hardware","¿El sistema muestra un error de hardware?",None,"Revise controladores y periféricos.",302,None,None,False,False),
        (302,"Hardware","¿El problema está relacionado con un periférico?","Pruebe otro puerto, cable y controlador.","Realice un diagnóstico general de hardware y registre síntomas.",None,None,None,False,True),
        (400,"Rendimiento","¿El uso de CPU supera aproximadamente el 80%?",None,None,401,402,None,False,False),
        (401,"Rendimiento","¿Hay un proceso no esencial consumiendo CPU?","Identifique el proceso y cierre solo procesos no esenciales.","Si el proceso es esencial, documente el servicio y escale.",None,None,None,False,True),
        (402,"Rendimiento","¿La memoria RAM supera aproximadamente el 80%?","Cierre aplicaciones innecesarias y revise programas de inicio.","Revise espacio libre, programas de inicio, actualizaciones y almacenamiento.",None,None,None,False,False),
        (500,"Impresora","¿La impresora está encendida?",None,"Conecte la impresora a la alimentación.",501,None,None,False,False),
        (501,"Impresora","¿La impresora aparece disponible en el sistema?",None,"Compruebe conexión, IP y vuelva a agregarla.",502,None,None,False,False),
        (502,"Impresora","¿El documento queda detenido en la cola?","Cancele trabajos pendientes y reinicie el servicio de cola.","Revise papel, tinta/tóner, atascos y controlador.",None,None,None,False,False),
        (600,"Software","¿La aplicación abre correctamente?",None,"Repare o reinstale la aplicación y compruebe requisitos y permisos.",601,None,None,False,False),
        (601,"Software","¿El problema ocurre solo con un usuario?","Revise perfil, permisos y configuración del usuario.","Revise instalación, dependencias, actualizaciones y compatibilidad.",None,None,None,False,True),
    ]

    for row in pasos:
        pid,categoria,pregunta,sol_si,sol_no,sig_si,sig_no,_,esc_si,esc_no = row
        obj=db.session.get(PasoDecision,pid)
        if obj is None:
            obj=PasoDecision(id=pid)
            db.session.add(obj)
        obj.categoria=categoria
        obj.pregunta=pregunta
        obj.solucion_si=sol_si
        obj.solucion_no=sol_no
        obj.siguiente_si=sig_si
        obj.siguiente_no=sig_no
        obj.escalar_si=esc_si
        obj.escalar_no=esc_no

    datos=[
        ("Red","Sin conexión a Internet","El equipo no puede navegar.","Problemas de IP, DNS, adaptador o conexión.","Verificar conexión, IP, gateway y DNS.","Restablecer la conexión y validar parámetros de red.","Alta",False),
        ("Wi-Fi","Wi-Fi desconectado","No detecta o no conecta a la red inalámbrica.","Adaptador, señal o configuración incorrecta.","Verificar Wi-Fi, señal, contraseña y DHCP.","Activar adaptador y reconectar.","Media",False),
        ("Hardware","Equipo no enciende","No inicia el sistema.","Alimentación o componente defectuoso.","Revisar fuente, cargador, toma y componentes.","Corregir alimentación o escalar.","Alta",True),
        ("Rendimiento","Equipo lento","Aplicaciones tardan en responder.","CPU/RAM elevada, almacenamiento o procesos.","Revisar Administrador de tareas y almacenamiento.","Cerrar procesos y realizar mantenimiento.","Media",False),
        ("Impresora","Impresora no imprime","Documentos permanecen en cola.","Cola, conexión o controlador.","Revisar cola, conexión y servicio.","Cancelar trabajos y reiniciar servicio.","Media",False),
        ("Software","Aplicación no inicia","El programa se cierra o no responde.","Archivos, permisos o incompatibilidad.","Revisar permisos, actualizar y reparar/reinstalar.","Reparar o reinstalar.","Media",False),
    ]
    for d in datos:
        categoria,problema,sintomas,causa,procedimiento,solucion,prioridad,escalar=d
        obj=Conocimiento.query.filter_by(categoria=categoria,problema=problema).first()
        if obj is None:
            obj=Conocimiento(categoria=categoria,problema=problema)
            db.session.add(obj)
        obj.sintomas=sintomas; obj.causa=causa; obj.procedimiento=procedimiento
        obj.solucion=solucion; obj.prioridad=prioridad; obj.requiere_escalamiento=escalar

    db.session.commit()

if __name__ == "__main__":
    from app import app
    with app.app_context():
        cargar_datos()
