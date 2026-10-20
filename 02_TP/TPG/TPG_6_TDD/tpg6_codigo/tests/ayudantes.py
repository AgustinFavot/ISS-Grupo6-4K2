"""Dobles de prueba y datos evidentes compartidos por los tests."""
from datetime import date, datetime

from eco_harmony.dominio import Visitante

MARTES = date(2026, 10, 20)
AHORA_MARTES_8 = datetime(2026, 10, 20, 8, 0)


class RelojFijo:
    """Reloj controlado por el test (aislamiento del tiempo real)."""

    def __init__(self, momento: datetime) -> None:
        self.momento = momento

    def ahora(self) -> datetime:
        return self.momento


class NotificadorEspia:
    """Registra los mails 'enviados' para poder verificarlos."""

    def __init__(self) -> None:
        self.enviados: list[dict] = []

    def enviar(self, destinatario: str, asunto: str, cuerpo: str) -> None:
        self.enviados.append({"destinatario": destinatario,
                              "asunto": asunto, "cuerpo": cuerpo})


def crear_visitante(nombre="Ana", dni="30123456", edad=25, talle=None):
    return Visitante(nombre=nombre, dni=dni, edad=edad, talle=talle)


def crear_visitantes(cantidad, talle=None):
    """Visitantes con DNI distintos: 30000000, 30000001, ..."""
    return [crear_visitante(nombre=f"Visitante {i}", dni=str(30000000 + i),
                            talle=talle)
            for i in range(cantidad)]
