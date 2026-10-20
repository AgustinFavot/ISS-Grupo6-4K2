"""Las seis pruebas de usuario de la tarjeta de la US."""
from datetime import date, datetime

import pytest

from eco_harmony.errores import (
    ActividadInexistenteError,
    ParqueCerradoError,
    SinCupoError,
    TalleRequeridoError,
    TerminosNoAceptadosError,
)
from tests.ayudantes import crear_visitante, crear_visitantes


def test_inscribirse_con_cupo_datos_completos_y_terminos_pasa(
        inscribir, notificador, titular):
    visitante = crear_visitante(talle="M")

    inscripcion = inscribir(actividad="Tirolesa", hora=11,
                            visitantes=[visitante])

    assert inscripcion.actividad.nombre == "Tirolesa"
    assert inscripcion.visitantes == (visitante,)
    assert len(notificador.enviados) == 1
    assert notificador.enviados[0]["destinatario"] == titular.email


def test_inscribirse_a_turno_sin_cupo_falla(inscribir):
    inscribir(visitantes=crear_visitantes(8))  # Safari: cupo 8

    with pytest.raises(SinCupoError):
        inscribir(visitantes=[crear_visitante(dni="40111222")])


def test_inscribirse_sin_talle_cuando_la_actividad_no_lo_requiere_pasa(
        inscribir):
    inscripcion = inscribir(actividad="Jardinería",
                            visitantes=[crear_visitante(talle=None)])

    assert inscripcion.visitantes[0].talle is None


def test_inscribirse_en_dia_que_el_parque_esta_cerrado_falla(inscribir,
                                                             reloj):
    reloj.momento = datetime(2026, 10, 18, 10, 0)  # domingo

    with pytest.raises(ParqueCerradoError):
        inscribir(fecha=date(2026, 10, 19), hora=9)  # lunes


def test_inscribirse_a_actividad_no_disponible_falla(inscribir):
    with pytest.raises(ActividadInexistenteError):
        inscribir(actividad="Buceo")


def test_inscribirse_sin_aceptar_terminos_falla(inscribir):
    with pytest.raises(TerminosNoAceptadosError):
        inscribir(acepta_terminos=False)


def test_inscribirse_sin_talle_requerido_por_la_actividad_falla(inscribir):
    with pytest.raises(TalleRequeridoError):
        inscribir(actividad="Palestra",
                  visitantes=[crear_visitante(talle=None)])
