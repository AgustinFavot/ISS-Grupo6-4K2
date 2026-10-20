"""Cupos por turno y selección de actividades disponibles."""
import pytest

from eco_harmony.errores import SinCupoError, TerminosNoAceptadosError
from tests.ayudantes import MARTES, crear_visitante, crear_visitantes


@pytest.mark.parametrize("actividad, cupo, talle", [
    ("Safari", 8, None),
    ("Palestra", 12, "L"),
    ("Jardinería", 12, None),
    ("Tirolesa", 10, "S"),
])
def test_completar_exactamente_el_cupo_pasa(inscribir, servicio, actividad,
                                            cupo, talle):
    inscribir(actividad=actividad, visitantes=crear_visitantes(cupo, talle))

    assert servicio.cupos_disponibles(actividad, MARTES, 10) == 0


def test_inscribir_mas_personas_que_el_cupo_restante_falla(inscribir):
    inscribir(visitantes=crear_visitantes(6))

    with pytest.raises(SinCupoError):
        inscribir(visitantes=[crear_visitante(dni="40000001"),
                              crear_visitante(dni="40000002"),
                              crear_visitante(dni="40000003")])


def test_cupos_disponibles_descuenta_los_inscriptos(inscribir, servicio):
    inscribir(visitantes=crear_visitantes(3))

    assert servicio.cupos_disponibles("Safari", MARTES, 10) == 5


def test_el_cupo_es_independiente_por_turno(inscribir, servicio):
    inscribir(hora=10, visitantes=crear_visitantes(8))

    assert servicio.cupos_disponibles("Safari", MARTES, 11) == 8


def test_actividades_disponibles_excluye_las_que_no_tienen_cupo(inscribir,
                                                                servicio):
    inscribir(visitantes=crear_visitantes(8))

    assert servicio.actividades_disponibles(MARTES, 10) == [
        "Tirolesa", "Palestra", "Jardinería"]


def test_horarios_disponibles_excluye_turnos_sin_cupo(inscribir, servicio):
    inscribir(hora=10, visitantes=crear_visitantes(8))

    assert 10 not in servicio.horarios_disponibles("Safari", MARTES)
    assert 11 in servicio.horarios_disponibles("Safari", MARTES)


def test_inscripcion_rechazada_no_ocupa_cupo_ni_envia_mail(inscribir,
                                                           servicio,
                                                           notificador):
    with pytest.raises(TerminosNoAceptadosError):
        inscribir(acepta_terminos=False)

    assert servicio.cupos_disponibles("Safari", MARTES, 10) == 8
    assert notificador.enviados == []
