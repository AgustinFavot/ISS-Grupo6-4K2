import pytest

from eco_harmony.dominio import Usuario
from eco_harmony.repositorio import RepositorioInscripciones
from eco_harmony.servicio import ServicioInscripcion
from tests.ayudantes import (
    AHORA_MARTES_8,
    MARTES,
    NotificadorEspia,
    RelojFijo,
    crear_visitante,
)


@pytest.fixture
def reloj():
    return RelojFijo(AHORA_MARTES_8)


@pytest.fixture
def notificador():
    return NotificadorEspia()


@pytest.fixture
def servicio(reloj, notificador):
    return ServicioInscripcion(reloj, notificador, RepositorioInscripciones())


@pytest.fixture
def titular():
    """Usuario logueado mockeado (FAQ 19)."""
    return Usuario(nombre="Ana Pérez", email="ana@example.com")


@pytest.fixture
def inscribir(servicio, titular):
    """Inscripción válida por defecto; cada test cambia solo lo que prueba."""
    def _inscribir(actividad="Safari", fecha=MARTES, hora=10,
                   visitantes=None, cantidad=None, acepta_terminos=True):
        if visitantes is None:
            visitantes = [crear_visitante()]
        if cantidad is None:
            cantidad = len(visitantes)
        return servicio.inscribir(titular, actividad, fecha, hora, cantidad,
                                  visitantes, acepta_terminos)
    return _inscribir
