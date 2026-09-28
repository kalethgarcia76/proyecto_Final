from flask import Blueprint, render_template
from models.ticket import Ticket

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    total = Ticket.query.count()
    abiertos = Ticket.query.filter(Ticket.estado != "Cerrado").count()
    return render_template("index.html", total=total, abiertos=abiertos)
