from flask import Flask
from config import Config

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(Config)  

    from routes.routes import route_bp, main_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(route_bp, url_prefix="/api")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="127.0.0.1", port=5000, debug=True)