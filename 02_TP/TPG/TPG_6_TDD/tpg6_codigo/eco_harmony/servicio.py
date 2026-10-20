"""Servicio de aplicación de la US «Inscribirme a actividad»."""
import re
from datetime import date, timedelta
from typing import Sequence

from eco_harmony import calendario
from eco_harmony.dominio import (
    CATALOGO_ACTIVIDADES,
    TALLES_VALIDOS,
    Actividad,
    Inscripcion,
    Turno,
    Usuario,
    Visitante,
    generar_codigo_qr,
)
from eco_harmony.errores import (
    ActividadInexistenteError,
    CantidadPersonasInvalidaError,
    DatosVisitanteInvalidosError,
    EdadInsuficienteError,
    FueraDeVentanaError,
    HorarioNoDisponibleError,
    InscripcionError,
    ParqueCerradoError,
    SinCupoError,
    SuperposicionHorariaError,
    TalleInvalidoError,
    TalleRequeridoError,
    TerminosNoAceptadosError,
)
from eco_harmony.mensajes import componer_confirmacion
from eco_harmony.puertos import Notificador, Reloj
from eco_harmony.repositorio import RepositorioInscripciones

ANTICIPACION_MAXIMA = timedelta(hours=24)
CIERRE_PREVIO_AL_TURNO = timedelta(minutes=15)
PATRON_DNI = re.compile(r"\d{7,8}")


class ServicioInscripcion:
    """Coordina la selección de turno y la inscripción de visitantes."""

    def __init__(self, reloj: Reloj, notificador: Notificador,
                 repositorio: RepositorioInscripciones) -> None:
        self._reloj = reloj
        self._notificador = notificador
        self._repositorio = repositorio

    # --- Consultas para la selección (CA 1 y 2, FAQ 8) ---

    def cupos_disponibles(self, nombre_actividad: str, fecha: date,
                          hora: int) -> int:
        actividad = self._obtener_actividad(nombre_actividad)
        ocupados = self._repositorio.lugares_ocupados(actividad.nombre,
                                                      Turno(fecha, hora))
        return actividad.cupo_por_turno - ocupados

    def actividades_disponibles(self, fecha: date, hora: int) -> list[str]:
        if not self.turno_habilitado(fecha, hora):
            return []
        return [nombre for nombre in CATALOGO_ACTIVIDADES
                if self.cupos_disponibles(nombre, fecha, hora) > 0]

    def horarios_disponibles(self, nombre_actividad: str,
                             fecha: date) -> list[int]:
        self._obtener_actividad(nombre_actividad)
        return [hora for hora in calendario.horas_de_turno()
                if self.turno_habilitado(fecha, hora)
                and self.cupos_disponibles(nombre_actividad, fecha, hora) > 0]

    # --- Comando principal ---

    def inscribir(self, titular: Usuario, nombre_actividad: str, fecha: date,
                  hora: int, cantidad_personas: int,
                  visitantes: Sequence[Visitante],
                  acepta_terminos: bool) -> Inscripcion:
        actividad = self._obtener_actividad(nombre_actividad)
        turno = self._validar_turno(fecha, hora)
        self._validar_cantidad(cantidad_personas, visitantes)
        for visitante in visitantes:
            self._validar_visitante(visitante, actividad)
        self._validar_cupo(actividad, turno, cantidad_personas)
        self._validar_superposicion(turno, visitantes)
        if not acepta_terminos:
            raise TerminosNoAceptadosError(
                f"Debe aceptar los términos y condiciones de "
                f"{actividad.nombre}.")
        inscripcion = self._registrar(titular, actividad, turno, visitantes)
        asunto, cuerpo = componer_confirmacion(inscripcion)
        self._notificador.enviar(titular.email, asunto, cuerpo)
        return inscripcion

    # --- Validaciones ---

    def _obtener_actividad(self, nombre_actividad: str) -> Actividad:
        try:
            return CATALOGO_ACTIVIDADES[nombre_actividad]
        except KeyError:
            raise ActividadInexistenteError(
                f"La actividad {nombre_actividad!r} no existe.") from None

    def _validar_turno(self, fecha: date, hora: int) -> Turno:
        if not calendario.parque_abierto(fecha):
            raise ParqueCerradoError(f"El parque está cerrado el {fecha}.")
        if not calendario.es_hora_de_turno(hora):
            raise HorarioNoDisponibleError(f"No hay turno a las {hora} hs.")
        turno = Turno(fecha, hora)
        anticipacion = turno.inicio - self._reloj.ahora()
        if anticipacion < CIERRE_PREVIO_AL_TURNO:
            raise FueraDeVentanaError(
                "La inscripción cierra 15 minutos antes del turno.")
        if anticipacion > ANTICIPACION_MAXIMA:
            raise FueraDeVentanaError(
                "Solo se puede inscribir dentro de las 24 hs previas.")
        return turno

    def turno_habilitado(self, fecha: date, hora: int) -> bool:
        """Parque abierto, hora de turno y dentro de la ventana."""
        try:
            self._validar_turno(fecha, hora)
        except InscripcionError:
            return False
        return True

    @staticmethod
    def _validar_cantidad(cantidad_personas: int,
                          visitantes: Sequence[Visitante]) -> None:
        if cantidad_personas < 1:
            raise CantidadPersonasInvalidaError(
                "Debe inscribir al menos una persona.")
        if cantidad_personas != len(visitantes):
            raise CantidadPersonasInvalidaError(
                "La cantidad de personas no coincide con los visitantes "
                "ingresados.")

    @staticmethod
    def _validar_visitante(visitante: Visitante,
                           actividad: Actividad) -> None:
        if not visitante.nombre.strip():
            raise DatosVisitanteInvalidosError(
                "Completá el nombre de cada participante.")
        if not PATRON_DNI.fullmatch(visitante.dni):
            raise DatosVisitanteInvalidosError(
                f"{visitante.nombre}: el DNI debe tener 7 u 8 números.")
        if isinstance(visitante.edad, bool) or visitante.edad < 0:
            raise DatosVisitanteInvalidosError(
                f"{visitante.nombre}: la edad no es válida.")
        if visitante.edad < actividad.edad_minima:
            raise EdadInsuficienteError(
                f"{visitante.nombre}: {actividad.nombre} requiere "
                f"{actividad.edad_minima} años o más.")
        if actividad.requiere_talle:
            if not visitante.talle:
                raise TalleRequeridoError(
                    f"{visitante.nombre}: elegí un talle de vestimenta, "
                    f"{actividad.nombre} lo requiere.")
            if visitante.talle not in TALLES_VALIDOS:
                raise TalleInvalidoError(
                    f"{visitante.nombre}: el talle {visitante.talle!r} no "
                    f"existe.")

    def _validar_cupo(self, actividad: Actividad, turno: Turno,
                      cantidad_personas: int) -> None:
        disponibles = self.cupos_disponibles(actividad.nombre, turno.fecha,
                                             turno.hora)
        if cantidad_personas > disponibles:
            raise SinCupoError(
                f"{actividad.nombre} tiene {disponibles} lugares en ese "
                f"turno.")

    def _validar_superposicion(self, turno: Turno,
                               visitantes: Sequence[Visitante]) -> None:
        dnis = [visitante.dni for visitante in visitantes]
        if len(dnis) != len(set(dnis)):
            raise SuperposicionHorariaError(
                "Un mismo DNI figura más de una vez en la inscripción.")
        for dni in dnis:
            if self._repositorio.dni_inscripto_en_turno(dni, turno):
                raise SuperposicionHorariaError(
                    f"El DNI {dni} ya está inscripto en ese horario.")

    def _registrar(self, titular: Usuario, actividad: Actividad,
                   turno: Turno,
                   visitantes: Sequence[Visitante]) -> Inscripcion:
        numero = self._repositorio.proximo_numero()
        inscripcion = Inscripcion(
            numero=numero,
            titular=titular,
            actividad=actividad,
            turno=turno,
            visitantes=tuple(visitantes),
            codigos_qr=tuple(generar_codigo_qr(numero, visitante.dni)
                             for visitante in visitantes),
        )
        self._repositorio.guardar(inscripcion)
        return inscripcion
