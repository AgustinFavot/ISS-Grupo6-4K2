"""Días de apertura, horario de turnos y ventana de inscripción."""
from datetime import date, datetime

import pytest

from eco_harmony.errores import (
    FueraDeVentanaError,
    HorarioNoDisponibleError,
    ParqueCerradoError,
)
from tests.ayudantes import MARTES


@pytest.mark.parametrize("ahora, fecha_turno", [
    (datetime(2026, 10, 18, 10, 0), date(2026, 10, 19)),  # lunes
    (datetime(2026, 12, 24, 10, 0), date(2026, 12, 25)),  # Navidad
    (datetime(2026, 12, 31, 10, 0), date(2027, 1, 1)),    # Año Nuevo
])
def test_inscribirse_en_dia_cerrado_falla(inscribir, reloj, ahora,
                                          fecha_turno):
    reloj.momento = ahora

    with pytest.raises(ParqueCerradoError):
        inscribir(fecha=fecha_turno, hora=9)


@pytest.mark.parametrize("hora", [8, 18, 19])
def test_inscribirse_fuera_del_horario_de_turnos_falla(inscribir, hora):
    with pytest.raises(HorarioNoDisponibleError):
        inscribir(hora=hora)


@pytest.mark.parametrize("hora", [9, 17])
def test_inscribirse_en_primer_y_ultimo_turno_pasa(inscribir, hora):
    assert inscribir(hora=hora).turno.hora == hora


def test_inscribirse_exactamente_24_hs_antes_pasa(inscribir, reloj):
    reloj.momento = datetime(2026, 10, 20, 10, 0)

    inscripcion = inscribir(fecha=date(2026, 10, 21), hora=10)

    assert inscripcion.turno.fecha == date(2026, 10, 21)


def test_inscribirse_con_mas_de_24_hs_de_anticipacion_falla(inscribir,
                                                            reloj):
    reloj.momento = datetime(2026, 10, 20, 9, 59)

    with pytest.raises(FueraDeVentanaError):
        inscribir(fecha=date(2026, 10, 21), hora=10)


def test_inscribirse_exactamente_15_minutos_antes_pasa(inscribir, reloj):
    reloj.momento = datetime(2026, 10, 20, 9, 45)

    assert inscribir(hora=10).turno.hora == 10


def test_inscribirse_a_menos_de_15_minutos_del_turno_falla(inscribir,
                                                           reloj):
    reloj.momento = datetime(2026, 10, 20, 9, 46)

    with pytest.raises(FueraDeVentanaError):
        inscribir(hora=10)


def test_inscribirse_a_turno_ya_iniciado_falla(inscribir, reloj):
    reloj.momento = datetime(2026, 10, 20, 10, 30)

    with pytest.raises(FueraDeVentanaError):
        inscribir(hora=10)


def test_horarios_disponibles_respeta_ventana_y_cierre(servicio, reloj):
    reloj.momento = datetime(2026, 10, 20, 15, 50)

    assert servicio.horarios_disponibles("Safari", MARTES) == [17]


def test_actividades_disponibles_vacia_si_el_turno_no_esta_habilitado(
        servicio):
    assert servicio.actividades_disponibles(MARTES, 18) == []
