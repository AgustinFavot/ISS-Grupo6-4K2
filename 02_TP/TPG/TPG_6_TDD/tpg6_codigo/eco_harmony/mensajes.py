"""Composición del mail de confirmación de la inscripción."""
from eco_harmony.dominio import Inscripcion


def componer_confirmacion(inscripcion: Inscripcion) -> tuple[str, str]:
    """Devuelve (asunto, cuerpo) con el resumen y los QR (FAQ 28)."""
    numero = f"{inscripcion.numero:06d}"
    asunto = (f"EcoHarmony Park - Inscripción N° {numero} - "
              f"{inscripcion.actividad.nombre}")
    lineas = [
        f"Inscripción N° {numero}",
        f"Actividad: {inscripcion.actividad.nombre}",
        f"Fecha: {inscripcion.turno.fecha:%d/%m/%Y}",
        f"Horario: {inscripcion.turno.hora:02d}:00",
        f"Cantidad de personas: {len(inscripcion.visitantes)}",
        "Participantes:",
    ]
    for visitante, codigo_qr in zip(inscripcion.visitantes,
                                    inscripcion.codigos_qr):
        talle = f" - Talle {visitante.talle}" if visitante.talle else ""
        lineas.append(
            f"- {visitante.nombre} - DNI {visitante.dni} - "
            f"{visitante.edad} años{talle} - QR: {codigo_qr}"
        )
    return asunto, "\n".join(lineas)
