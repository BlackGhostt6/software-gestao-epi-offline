from flask import Flask
import threading
import time
import webview

app = Flask(__name__)

# 👉 importa teu blueprint aqui
from controller.routes import api_routes
app.register_blueprint(api_routes)

def run_flask():
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)

def start_app():
    # espera o flask subir
    time.sleep(1.5)

    webview.create_window(
        "Sistema de Gestão de EPIs",
        "http://127.0.0.1:5000"
    )
    webview.start()

if __name__ == "__main__":
    t = threading.Thread(target=run_flask, daemon=True)
    t.start()

    start_app()