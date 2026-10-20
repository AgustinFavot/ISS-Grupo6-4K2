"""Levanta la interfaz web: python app.py y abrir http://127.0.0.1:5000."""
from eco_harmony.web import crear_app

if __name__ == "__main__":
    crear_app().run(host="127.0.0.1", port=5000, debug=False)
