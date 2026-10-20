"""Reglas de calendario del parque y de los turnos de actividades."""
from datetime import date

HORA_PRIMER_TURNO = 9
HORA_ULTIMO_TURNO = 17  # A las 18:00 no hay turno: es la cota superior.
LUNES = 0
FERIADOS_CERRADO = frozenset({(12, 25), (1, 1)})  # (mes, día)


def parque_abierto(fecha: date) -> bool:
    """El parque abre todos los días menos los lunes, el 25/12 y el 1/1."""
    if fecha.weekday() == LUNES:
        return False
    return (fecha.month, fecha.day) not in FERIADOS_CERRADO


def es_hora_de_turno(hora: int) -> bool:
    """Hay un turno por hora entre las 9 y las 17 (inicio)."""
    return HORA_PRIMER_TURNO <= hora <= HORA_ULTIMO_TURNO


def horas_de_turno() -> range:
    return range(HORA_PRIMER_TURNO, HORA_ULTIMO_TURNO + 1)
