from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for, session, flash

from werkzeug.security import check_password_hash\nfrom sqlalchemy import or_

from database.database import db
from models.usuario import Usuario, RegistroAcceso


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if session.get("usuario_id"):
        return redirect(url_for("main.inicio"))

    if request.method == "POST":
        usuario_texto = request.form.get("usuario", "").strip()
        password = request.form.get("password", "")

        if not usuario_texto or not password:
            flash("Completa el usuario y la contraseña.", "error")
            return render_template("login.html", usuario=usuario_texto)

        usuario = Usuario.query.filter(
            db.or_(
                Usuario.usuario == usuario_texto,
                Usuario.correo == usuario_texto
            )
        ).first()

        ip = request.headers.get("X-Forwarded-For", request.remote_addr)

        if usuario and usuario.activo and check_password_hash(
            usuario.password_hash,
            password
        ):
            usuario.ultimo_acceso = datetime.utcnow()

            registro = RegistroAcceso(
                usuario_id=usuario.id,
                usuario=usuario.usuario,
                ip=ip,
                exitoso=True,
                motivo="Inicio de sesión correcto"
            )

            db.session.add(registro)
            db.session.commit()

            session.clear()
            session["usuario_id"] = usuario.id
            session["usuario"] = usuario.usuario
            session["nombre"] = usuario.nombre
            session["rol"] = usuario.rol

            flash(f"Bienvenido, {usuario.nombre}.", "success")
            return redirect(url_for("main.inicio"))

        registro = RegistroAcceso(
            usuario_id=usuario.id if usuario else None,
            usuario=usuario_texto,
            ip=ip,
            exitoso=False,
            motivo="Credenciales inválidas o usuario inactivo"
        )

        db.session.add(registro)
        db.session.commit()

        flash("Usuario o contraseña incorrectos.", "error")

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Sesión cerrada correctamente.", "success")
    return redirect(url_for("auth.login"))
