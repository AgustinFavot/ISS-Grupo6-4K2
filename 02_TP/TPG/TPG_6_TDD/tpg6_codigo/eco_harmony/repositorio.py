"""Almacenamiento en memoria de las inscripciones confirmadas."""
from eco_harmony.dominio import Inscripcion, Turno


class RepositorioInscripciones:

    def __init__(self) -> None:
        self._inscripciones: list[Inscripcion] = []

    def proximo_numero(self) -> int:
        return len(self._inscripciones) + 1

    def guardar(self, inscripcion: Inscripcion) -> None:
        self._inscripciones.append(inscripcion)

    def lugares_ocupados(self, nombre_actividad: str, turno: Turno) -> int:
        return sum(
            len(inscripcion.visitantes)
            for inscripcion in self._inscripciones
            if inscripcion.actividad.nombre == nombre_actividad
            and inscripcion.turno == turno
        )

    def dni_inscripto_en_turno(self, dni: str, turno: Turno) -> bool:
        return any(
            inscripcion.turno == turno
            and any(visitante.dni == dni
                    for visitante in inscripcion.visitantes)
            for inscripcion in self._inscripciones
        )
