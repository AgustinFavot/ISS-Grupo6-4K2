"""Dependencias externas del servicio: reloj y envío de mails."""
from datetime import datetime
from typing import Protocol


class Reloj(Protocol):
    def ahora(self) -> datetime:
        ...


class Notificador(Protocol):
    def enviar(self, destinatario: str, asunto: str, cuerpo: str) -> None:
        ...


class RelojSistema:
    """Reloj real utilizado en ejecución."""

    def ahora(self) -> datetime:
        return datetime.now()


class RelojFijo:
    """Reloj detenido en un momento dado (pruebas y demostraciones)."""

    def __init__(self, momento: datetime) -> None:
        self.momento = momento

    def ahora(self) -> datetime:
        return self.momento


class NotificadorSimulado:
    """Simula el envío del mail (habilitado por el FAQ 5)."""

    def enviar(self, destinatario: str, asunto: str, cuerpo: str) -> None:
        print(f"Mail enviado a {destinatario}\n{asunto}\n\n{cuerpo}")


class BandejaSimulada:
    """Guarda los mails 'enviados' para mostrarlos en la interfaz."""

    def __init__(self) -> None:
        self.enviados: list[dict] = []

    def enviar(self, destinatario: str, asunto: str, cuerpo: str) -> None:
        self.enviados.append({"destinatario": destinatario,
                              "asunto": asunto, "cuerpo": cuerpo})

    @property
    def ultimo(self) -> dict:
        return self.enviados[-1]
