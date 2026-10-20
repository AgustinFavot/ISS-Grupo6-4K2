"""Mail de confirmación: resumen de la inscripción y QR (FAQ 28)."""
from tests.ayudantes import crear_visitante


def test_mail_contiene_resumen_y_un_qr_por_participante(inscribir,
                                                        notificador):
    visitantes = [crear_visitante(nombre="Ana", dni="30123456", talle="M"),
                  crear_visitante(nombre="Luis", dni="31987654", talle="L")]

    inscripcion = inscribir(actividad="Tirolesa", hora=11,
                            visitantes=visitantes)

    cuerpo = notificador.enviados[0]["cuerpo"]
    assert "Actividad: Tirolesa" in cuerpo
    assert "Fecha: 20/10/2026" in cuerpo
    assert "Horario: 11:00" in cuerpo
    assert "Ana - DNI 30123456 - 25 años - Talle M" in cuerpo
    assert "Luis - DNI 31987654" in cuerpo
    for codigo_qr in inscripcion.codigos_qr:
        assert f"QR: {codigo_qr}" in cuerpo


def test_cada_participante_recibe_un_qr_distinto(inscribir):
    inscripcion = inscribir(visitantes=[crear_visitante(dni="30123456"),
                                        crear_visitante(dni="31987654")])

    assert len(set(inscripcion.codigos_qr)) == 2


def test_asunto_incluye_numero_de_inscripcion_y_actividad(inscribir,
                                                          notificador):
    inscribir(actividad="Safari")

    asunto = notificador.enviados[0]["asunto"]
    assert "N° 000001" in asunto
    assert "Safari" in asunto
