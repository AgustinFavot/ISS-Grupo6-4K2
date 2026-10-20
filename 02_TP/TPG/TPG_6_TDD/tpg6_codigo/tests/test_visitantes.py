"""Datos del visitante, talles, edades, cantidad y superposición."""
import pytest

from eco_harmony.errores import (
    CantidadPersonasInvalidaError,
    DatosVisitanteInvalidosError,
    EdadInsuficienteError,
    SuperposicionHorariaError,
    TalleInvalidoError,
)
from tests.ayudantes import crear_visitante, crear_visitantes


@pytest.mark.parametrize("talle", ["XS", "S", "M", "L", "XL", "XXL"])
def test_talles_validos_pasan(inscribir, talle):
    inscripcion = inscribir(actividad="Palestra",
                            visitantes=[crear_visitante(talle=talle)])

    assert inscripcion.visitantes[0].talle == talle


def test_talle_inexistente_falla(inscribir):
    with pytest.raises(TalleInvalidoError):
        inscribir(actividad="Tirolesa",
                  visitantes=[crear_visitante(talle="XXXL")])


@pytest.mark.parametrize("actividad, edad", [("Palestra", 11),
                                             ("Tirolesa", 7)])
def test_edad_menor_a_la_minima_falla(inscribir, actividad, edad):
    with pytest.raises(EdadInsuficienteError):
        inscribir(actividad=actividad,
                  visitantes=[crear_visitante(edad=edad, talle="S")])


@pytest.mark.parametrize("actividad, edad", [("Palestra", 12),
                                             ("Tirolesa", 8)])
def test_edad_igual_a_la_minima_pasa(inscribir, actividad, edad):
    inscripcion = inscribir(actividad=actividad,
                            visitantes=[crear_visitante(edad=edad,
                                                        talle="S")])

    assert inscripcion.visitantes[0].edad == edad


@pytest.mark.parametrize("actividad", ["Safari", "Jardinería"])
def test_actividades_sin_limite_de_edad_aceptan_bebes(inscribir, actividad):
    assert inscribir(actividad=actividad,
                     visitantes=[crear_visitante(edad=0)])


@pytest.mark.parametrize("visitante", [
    crear_visitante(nombre=""),
    crear_visitante(dni="AB123456"),
    crear_visitante(dni="123456"),
    crear_visitante(dni="123456789"),
    crear_visitante(edad=-1),
])
def test_datos_de_visitante_invalidos_fallan(inscribir, visitante):
    with pytest.raises(DatosVisitanteInvalidosError):
        inscribir(visitantes=[visitante])


@pytest.mark.parametrize("cantidad", [0, 2])
def test_cantidad_que_no_coincide_con_visitantes_falla(inscribir, cantidad):
    with pytest.raises(CantidadPersonasInvalidaError):
        inscribir(visitantes=[crear_visitante()], cantidad=cantidad)


def test_inscribir_varias_personas_en_una_transaccion_pasa(inscribir):
    inscripcion = inscribir(actividad="Jardinería",
                            visitantes=crear_visitantes(12))

    assert len(inscripcion.visitantes) == 12


def test_mismo_dni_en_otra_actividad_del_mismo_horario_falla(inscribir):
    inscribir(actividad="Safari", hora=10)

    with pytest.raises(SuperposicionHorariaError):
        inscribir(actividad="Jardinería", hora=10)


def test_mismo_dni_en_distinto_horario_pasa(inscribir):
    inscribir(actividad="Safari", hora=10)

    assert inscribir(actividad="Jardinería", hora=11)


def test_dni_repetido_dentro_de_la_misma_inscripcion_falla(inscribir):
    with pytest.raises(SuperposicionHorariaError):
        inscribir(visitantes=[crear_visitante(), crear_visitante()])
