from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from sqlalchemy import or_
from werkzeug.security import check_password_hash, generate_password_hash

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
            or_(
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


@auth_bp.route("/registro", methods=["GET", "POST"])
def registro():
    if session.get("usuario_id"):
        return redirect(url_for("main.inicio"))

    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        usuario_texto = request.form.get("usuario", "").strip().lower()
        correo = request.form.get("correo", "").strip().lower()
        password = request.form.get("password", "")
        confirmar = request.form.get("confirmar", "")

        if not all([nombre, usuario_texto, correo, password, confirmar]):
            flash("Completa todos los campos.", "error")
            return render_template(
                "registro.html",
                nombre=nombre,
                usuario=usuario_texto,
                correo=correo
            )

        if len(nombre) < 3:
            flash("El nombre debe tener al menos 3 caracteres.", "error")
            return render_template("registro.html", nombre=nombre, usuario=usuario_texto, correo=correo)

        if len(usuario_texto) < 4 or not usuario_texto.replace("_", "").replace("-", "").isalnum():
            flash("El usuario debe tener al menos 4 caracteres y solo puede contener letras, números, guion o guion bajo.", "error")
            return render_template("registro.html", nombre=nombre, usuario=usuario_texto, correo=correo)

        if "@" not in correo or "." not in correo.split("@")[-1]:
            flash("Ingresa un correo electrónico válido.", "error")
            return render_template("registro.html", nombre=nombre, usuario=usuario_texto, correo=correo)

        if len(password) < 8:
            flash("La contraseña debe tener al menos 8 caracteres.", "error")
            return render_template("registro.html", nombre=nombre, usuario=usuario_texto, correo=correo)

        if password != confirmar:
            flash("Las contraseñas no coinciden.", "error")
            return render_template("registro.html", nombre=nombre, usuario=usuario_texto, correo=correo)

        existente = Usuario.query.filter(
            or_(
                Usuario.usuario == usuario_texto,
                Usuario.correo == correo
            )
        ).first()

        if existente:
            if existente.usuario == usuario_texto:
                flash("Ese nombre de usuario ya está registrado.", "error")
            else:
                flash("Ese correo electrónico ya está registrado.", "error")

            return render_template(
                "registro.html",
                nombre=nombre,
                usuario=usuario_texto,
                correo=correo
            )

        nuevo_usuario = Usuario(
            nombre=nombre,
            usuario=usuario_texto,
            correo=correo,
            password_hash=generate_password_hash(password),
            rol="tecnico",
            activo=True
        )

        db.session.add(nuevo_usuario)
        db.session.commit()

        flash("Cuenta creada correctamente. Ya puedes iniciar sesión.", "success")
        return redirect(url_for("auth.login"))

    return render_template("registro.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Sesión cerrada correctamente.", "success")
    return redirect(url_for("auth.login"))
