"""Interfaz web responsive de la US «Inscribirme a actividad»."""
import os
from datetime import date, datetime, timedelta

import qrcode
import qrcode.image.svg
from flask import Flask, jsonify, render_template, request

from eco_harmony import calendario
from eco_harmony.dominio import (
    CATALOGO_ACTIVIDADES,
    TALLES,
    Inscripcion,
    Usuario,
    Visitante,
)
from eco_harmony.errores import InscripcionError
from eco_harmony.puertos import BandejaSimulada, RelojFijo, RelojSistema
from eco_harmony.repositorio import RepositorioInscripciones
from eco_harmony.servicio import ServicioInscripcion
from eco_harmony.web.terminos import TERMINOS_Y_CONDICIONES

DIAS_EN_CALENDARIO = 7
NOMBRES_DIAS = ("Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom")
TITULAR_MOCK = Usuario(nombre="Ana Pérez", email="ana.perez@example.com")


class SolicitudInvalida(ValueError):
    """El cuerpo de la solicitud no tiene el formato esperado."""


def crear_app(reloj=None, bandeja=None) -> Flask:
    """Arma la aplicación; las pruebas inyectan reloj y bandeja."""
    app = Flask(__name__)
    reloj = reloj or _reloj_por_defecto()
    bandeja = bandeja or BandejaSimulada()
    servicio = ServicioInscripcion(reloj, bandeja,
                                   RepositorioInscripciones())

    @app.get("/")
    def inicio():
        return render_template("index.html", titular=TITULAR_MOCK,
                               talles=TALLES)

    @app.get("/api/dias")
    def dias():
        hoy = reloj.ahora().date()
        return jsonify([_describir_dia(servicio, hoy + timedelta(days=n))
                        for n in range(DIAS_EN_CALENDARIO)])

    @app.get("/api/disponibilidad")
    def disponibilidad():
        try:
            fecha = date.fromisoformat(request.args.get("fecha", ""))
        except ValueError:
            return jsonify(error="Fecha inválida."), 400
        return jsonify(fecha=fecha.isoformat(),
                       actividades=[_describir_actividad(servicio, nombre,
                                                         fecha)
                                    for nombre in CATALOGO_ACTIVIDADES])

    @app.post("/api/inscripciones")
    def inscribir():
        try:
            datos = _leer_solicitud(request.get_json(silent=True))
        except SolicitudInvalida as error:
            return jsonify(error=str(error), tipo="SolicitudInvalida"), 400
        try:
            inscripcion = servicio.inscribir(TITULAR_MOCK, **datos)
        except InscripcionError as error:
            return jsonify(error=str(error),
                           tipo=type(error).__name__), 422
        return jsonify(inscripcion=_serializar(inscripcion),
                       mail=bandeja.ultimo), 201

    return app


def _reloj_por_defecto():
    """ECO_AHORA=AAAA-MM-DDTHH:MM fija la hora para demostraciones."""
    ahora = os.environ.get("ECO_AHORA")
    return RelojFijo(datetime.fromisoformat(ahora)) if ahora \
        else RelojSistema()


def _describir_dia(servicio, fecha: date) -> dict:
    habilitado = any(servicio.turno_habilitado(fecha, hora)
                     for hora in calendario.horas_de_turno())
    if habilitado:
        motivo = ""
    elif not calendario.parque_abierto(fecha):
        motivo = "Parque cerrado"
    else:
        motivo = "Fuera de las 24 hs"
    return {"fecha": fecha.isoformat(), "dia": NOMBRES_DIAS[fecha.weekday()],
            "numero": fecha.day, "habilitado": habilitado, "motivo": motivo}


def _describir_actividad(servicio, nombre: str, fecha: date) -> dict:
    actividad = CATALOGO_ACTIVIDADES[nombre]
    horarios = [{"hora": hora,
                 "cupos": servicio.cupos_disponibles(nombre, fecha, hora)}
                for hora in calendario.horas_de_turno()
                if servicio.turno_habilitado(fecha, hora)]
    return {"nombre": nombre, "cupo_por_turno": actividad.cupo_por_turno,
            "requiere_talle": actividad.requiere_talle,
            "edad_minima": actividad.edad_minima, "horarios": horarios,
            "terminos": TERMINOS_Y_CONDICIONES[nombre]}


def _leer_solicitud(cuerpo) -> dict:
    if not isinstance(cuerpo, dict):
        raise SolicitudInvalida("Se esperaba un objeto JSON.")
    try:
        visitantes = [
            Visitante(nombre=str(v.get("nombre", "")).strip(),
                      dni=str(v.get("dni", "")).strip(),
                      edad=_entero(v.get("edad"), "edad"),
                      talle=(v.get("talle") or None))
            for v in cuerpo["visitantes"]
        ]
        return {"nombre_actividad": str(cuerpo["actividad"]),
                "fecha": date.fromisoformat(cuerpo["fecha"]),
                "hora": _entero(cuerpo["hora"], "hora"),
                "cantidad_personas": _entero(cuerpo["cantidad"], "cantidad"),
                "visitantes": visitantes,
                "acepta_terminos": cuerpo.get("acepta_terminos") is True}
    except (KeyError, TypeError, AttributeError) as error:
        raise SolicitudInvalida(f"Falta o es inválido: {error}.") from None
    except ValueError as error:
        raise SolicitudInvalida(str(error)) from None


def _entero(valor, campo: str) -> int:
    if isinstance(valor, bool):
        raise SolicitudInvalida(f"El campo {campo} debe ser un número.")
    try:
        return int(valor)
    except (TypeError, ValueError):
        raise SolicitudInvalida(
            f"El campo {campo} debe ser un número.") from None


def _qr_svg(contenido: str) -> str:
    imagen = qrcode.make(contenido, box_size=10, border=2,
                         image_factory=qrcode.image.svg.SvgPathImage)
    return imagen.to_string(encoding="unicode")


def _serializar(inscripcion: Inscripcion) -> dict:
    return {
        "numero": f"{inscripcion.numero:06d}",
        "actividad": inscripcion.actividad.nombre,
        "fecha": inscripcion.turno.fecha.isoformat(),
        "hora": inscripcion.turno.hora,
        "visitantes": [
            {"nombre": v.nombre, "dni": v.dni, "edad": v.edad,
             "talle": v.talle, "qr": qr, "qr_svg": _qr_svg(qr)}
            for v, qr in zip(inscripcion.visitantes, inscripcion.codigos_qr)
        ],
    }
