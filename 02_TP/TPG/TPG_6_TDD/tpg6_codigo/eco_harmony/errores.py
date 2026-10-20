"""Excepciones de las reglas de negocio de la inscripción a actividades."""


class InscripcionError(Exception):
    """Error base: la inscripción no cumple una regla de negocio."""


class ActividadInexistenteError(InscripcionError):
    """La actividad no pertenece al conjunto ofrecido por el parque."""


class ParqueCerradoError(InscripcionError):
    """La fecha corresponde a un día en que el parque está cerrado."""


class HorarioNoDisponibleError(InscripcionError):
    """La hora no corresponde a un turno de actividad."""


class FueraDeVentanaError(InscripcionError):
    """El turno está fuera de la ventana de inscripción (24 hs / 15 min)."""


class SinCupoError(InscripcionError):
    """El turno no tiene cupo suficiente para las personas indicadas."""


class CantidadPersonasInvalidaError(InscripcionError):
    """La cantidad indicada no es válida o no coincide con los visitantes."""


class DatosVisitanteInvalidosError(InscripcionError):
    """Nombre, DNI o edad del visitante ausentes o inválidos."""


class TalleRequeridoError(InscripcionError):
    """La actividad exige talle de vestimenta y no se ingresó."""


class TalleInvalidoError(InscripcionError):
    """El talle ingresado no pertenece a los talles disponibles."""


class EdadInsuficienteError(InscripcionError):
    """El visitante no alcanza la edad mínima de la actividad."""


class TerminosNoAceptadosError(InscripcionError):
    """No se aceptaron los términos y condiciones de la actividad."""


class SuperposicionHorariaError(InscripcionError):
    """El visitante ya tiene una inscripción en un turno del mismo horario."""
