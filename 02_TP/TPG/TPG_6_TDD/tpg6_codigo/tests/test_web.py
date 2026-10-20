"""Pruebas de la interfaz web (API y página) con el cliente de Flask."""
import pytest

from eco_harmony.puertos import BandejaSimulada, RelojFijo
from eco_harmony.web import crear_app
from tests.ayudantes import AHORA_MARTES_8


@pytest.fixture
def bandeja():
    return BandejaSimulada()


@pytest.fixture
def cliente(bandeja):
    app = crear_app(reloj=RelojFijo(AHORA_MARTES_8), bandeja=bandeja)
    app.config["TESTING"] = True
    return app.test_client()


def solicitud_valida(**cambios):
    datos = {
        "actividad": "Tirolesa", "fecha": "2026-10-20", "hora": 11,
        "cantidad": 1, "acepta_terminos": True,
        "visitantes": [{"nombre": "Ana", "dni": "30123456", "edad": 25,
                        "talle": "M"}],
    }
    datos.update(cambios)
    return datos


def test_pagina_principal_usa_fuente_y_paleta_del_po(cliente):
    respuesta = cliente.get("/")
    css = cliente.get("/static/app.css").get_data(as_text=True)

    assert respuesta.status_code == 200
    assert "Inscribirme a una actividad" in respuesta.get_data(as_text=True)
    assert "Lato" in css
    for color in ("#386641", "#6a994e", "#a7c957", "#f2e8cf", "#bc4749"):
        assert color in css.lower()


def test_calendario_deshabilita_lunes_y_dias_fuera_de_ventana(cliente):
    dias = {dia["fecha"]: dia for dia in cliente.get("/api/dias").json}

    # Ahora: martes 20/10 a las 8:00; el turno de las 9 del miércoles
    # empieza en 25 hs, fuera de la ventana de 24 hs.
    assert dias["2026-10-20"]["habilitado"] is True
    assert dias["2026-10-21"]["habilitado"] is False
    assert dias["2026-10-21"]["motivo"] == "Fuera de las 24 hs"
    assert dias["2026-10-26"]["habilitado"] is False
    assert dias["2026-10-26"]["motivo"] == "Parque cerrado"


def test_disponibilidad_informa_cupos_y_terminos_por_actividad(cliente):
    datos = cliente.get("/api/disponibilidad?fecha=2026-10-20").json
    safari = next(a for a in datos["actividades"] if a["nombre"] == "Safari")

    assert safari["requiere_talle"] is False
    assert safari["horarios"][0] == {"hora": 9, "cupos": 8}
    assert [h["hora"] for h in safari["horarios"]] == list(range(9, 18))
    assert safari["terminos"]


def test_disponibilidad_con_fecha_invalida_responde_400(cliente):
    assert cliente.get("/api/disponibilidad?fecha=ayer").status_code == 400


def test_inscripcion_valida_devuelve_qr_y_mail_simulado(cliente, bandeja):
    respuesta = cliente.post("/api/inscripciones", json=solicitud_valida())

    assert respuesta.status_code == 201
    visitante = respuesta.json["inscripcion"]["visitantes"][0]
    assert visitante["qr"].startswith("EHP-ACT-")
    assert visitante["qr_svg"].lstrip().startswith("<svg")
    assert respuesta.json["mail"]["destinatario"] == bandeja.ultimo[
        "destinatario"]


def test_inscripcion_descuenta_el_cupo_mostrado(cliente):
    cliente.post("/api/inscripciones", json=solicitud_valida())

    datos = cliente.get("/api/disponibilidad?fecha=2026-10-20").json
    tirolesa = next(a for a in datos["actividades"]
                    if a["nombre"] == "Tirolesa")
    assert {"hora": 11, "cupos": 9} in tirolesa["horarios"]


def test_regla_de_negocio_incumplida_responde_422_con_motivo(cliente):
    respuesta = cliente.post("/api/inscripciones",
                             json=solicitud_valida(acepta_terminos=False))

    assert respuesta.status_code == 422
    assert respuesta.json["tipo"] == "TerminosNoAceptadosError"
    assert "términos" in respuesta.json["error"]


def test_talle_faltante_responde_422(cliente):
    visitantes = [{"nombre": "Ana", "dni": "30123456", "edad": 25,
                   "talle": ""}]
    respuesta = cliente.post("/api/inscripciones",
                             json=solicitud_valida(visitantes=visitantes))

    assert respuesta.status_code == 422
    assert respuesta.json["tipo"] == "TalleRequeridoError"


@pytest.mark.parametrize("cuerpo", [
    {},
    solicitud_valida(hora="once"),
    solicitud_valida(visitantes=[{"nombre": "Ana", "dni": "30123456",
                                  "edad": "veinte"}]),
])
def test_solicitud_mal_formada_responde_400(cliente, cuerpo):
    assert cliente.post("/api/inscripciones",
                        json=cuerpo).status_code == 400
