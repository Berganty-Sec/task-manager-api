from flask import Flask, jsonify
from .config import Config
from .extensions import db, jwt
from flask_cors import CORS
from flask import send_from_directory


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)

    db.init_app(app)
    jwt.init_app(app)

    from .routes.auth import auth_bp
    app.register_blueprint(auth_bp)
    from .routes.tasks import tasks_bp
    app.register_blueprint(tasks_bp)
    from .models import User  # Registra os models no SQLAlchemy

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})

    @app.get("/")
    def home():
        return send_from_directory("static", "ui.html")

    return app
