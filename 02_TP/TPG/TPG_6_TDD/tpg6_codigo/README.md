# TP6 - TDD: Inscribirme a actividad (EcoHarmony Park)

Requisitos: Python 3.10 o superior.

    pip install -r requirements.txt
    python -m pytest -v      # 70 pruebas (dominio + interfaz)
    python app.py            # interfaz en http://127.0.0.1:5000

La interfaz usa la hora real. Para una demostración con turnos abiertos se
puede fijar la hora (en Windows: set ECO_AHORA=2026-10-20T08:00):

    ECO_AHORA=2026-10-20T08:00 python app.py

Estructura:

    eco_harmony/        dominio y servicio de inscripción
    eco_harmony/web/    interfaz web responsive (Flask, HTML, CSS, JS)
    tests/              pruebas automatizadas (pytest)
    capturas/           capturas de la interfaz
