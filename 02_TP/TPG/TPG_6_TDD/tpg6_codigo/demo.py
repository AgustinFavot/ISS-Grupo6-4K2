"""Ejecución de ejemplo con reloj real y mail simulado."""
from datetime import timedelta

from eco_harmony.dominio import Usuario, Visitante
from eco_harmony.errores import InscripcionError
from eco_harmony.puertos import NotificadorSimulado, RelojSistema
from eco_harmony.repositorio import RepositorioInscripciones
from eco_harmony.servicio import ServicioInscripcion


def main() -> None:
    reloj = RelojSistema()
    servicio = ServicioInscripcion(reloj, NotificadorSimulado(),
                                   RepositorioInscripciones())
    titular = Usuario("Ana Pérez", "ana@example.com")
    for fecha in (reloj.ahora().date(),
                  reloj.ahora().date() + timedelta(days=1)):
        horarios = servicio.horarios_disponibles("Tirolesa", fecha)
        if horarios:
            break
    else:
        print("No hay turnos de Tirolesa en las próximas 24 hs.")
        return
    try:
        servicio.inscribir(titular, "Tirolesa", fecha, horarios[0], 1,
                           [Visitante("Ana", "30123456", 25, "M")], True)
    except InscripcionError as error:
        print(f"Inscripción rechazada: {error}")


if __name__ == "__main__":
    main()
