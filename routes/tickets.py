from flask import Blueprint, render_template, request, redirect, url_for
from database.database import db
from models.ticket import Ticket

tickets_bp = Blueprint("tickets", __name__)


@tickets_bp.route("/")
def listar():
    tickets = Ticket.query.order_by(Ticket.id.desc()).all()
    return render_template("tickets.html", tickets=tickets)


@tickets_bp.route("/nuevo", methods=["POST"])
def nuevo():
    ultimo = Ticket.query.order_by(Ticket.id.desc()).first()
    numero = (ultimo.id + 1) if ultimo else 1
    ticket = Ticket(
        codigo=f"TCK-{numero:05d}",
        titulo=request.form["titulo"],
        categoria=request.form["categoria"],
        prioridad=request.form.get("prioridad", "Media"),
        descripcion=request.form["descripcion"],
    )
    db.session.add(ticket)
    db.session.commit()
    return redirect(url_for("tickets.listar"))
