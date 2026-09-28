from flask import Blueprint, render_template

from models.ticket import Ticket
from models.conocimiento import Conocimiento


main_bp = Blueprint(
    "main",
    __name__
)


@main_bp.route("/")
def inicio():

    total_tickets = Ticket.query.count()

    tickets_abiertos = Ticket.query.filter(
        Ticket.estado != "Cerrado"
    ).count()

    soluciones = Conocimiento.query.count()

    return render_template(
        "index.html",
        total_tickets=total_tickets,
        tickets_abiertos=tickets_abiertos,
        soluciones=soluciones
    )