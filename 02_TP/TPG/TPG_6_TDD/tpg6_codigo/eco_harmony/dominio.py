"""Entidades del dominio de inscripción a actividades."""
from dataclasses import dataclass
from datetime import date, datetime, time
from typing import Optional

TALLES = ("XS", "S", "M", "L", "XL", "XXL")
TALLES_VALIDOS = frozenset(TALLES)


@dataclass(frozen=True)
class Actividad:
    """Actividad de una hora ofrecida por el parque."""

    nombre: str
    cupo_por_turno: int
    requiere_talle: bool
    edad_minima: int = 0


CATALOGO_ACTIVIDADES = {
    actividad.nombre: actividad
    for actividad in (
        Actividad("Tirolesa", cupo_por_turno=10, requiere_talle=True,
                  edad_minima=8),
        Actividad("Safari", cupo_por_turno=8, requiere_talle=False),
        Actividad("Palestra", cupo_por_turno=12, requiere_talle=True,
                  edad_minima=12),
        Actividad("Jardinería", cupo_por_turno=12, requiere_talle=False),
    )
}


@dataclass(frozen=True)
class Turno:
    """Turno de una actividad: fecha y hora de inicio."""

    fecha: date
    hora: int

    @property
    def inicio(self) -> datetime:
        return datetime.combine(self.fecha, time(self.hora))


@dataclass(frozen=True)
class Visitante:
    """Persona que participa de la actividad."""

    nombre: str
    dni: str
    edad: int
    talle: Optional[str] = None


@dataclass(frozen=True)
class Usuario:
    """Titular registrado que realiza la inscripción (sesión mockeada)."""

    nombre: str
    email: str


@dataclass(frozen=True)
class Inscripcion:
    """Inscripción confirmada a un turno de una actividad."""

    numero: int
    titular: Usuario
    actividad: Actividad
    turno: Turno
    visitantes: tuple[Visitante, ...]
    codigos_qr: tuple[str, ...]


def generar_codigo_qr(numero_inscripcion: int, dni: str) -> str:
    """Devuelve el contenido del QR de acceso de un visitante."""
    return f"EHP-ACT-{numero_inscripcion:06d}-{dni}"
