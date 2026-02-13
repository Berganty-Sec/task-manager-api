from flask_jwt_extended import create_access_token
from flask import Blueprint, request, jsonify
import bcrypt

from app.extensions import db
from app.models import User
from flask_jwt_extended import jwt_required, get_jwt_identity

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.post("/register")
def register():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    password = (data.get("password") or "")

# Validação de caractere Vazio
    if not username or not password:
        return jsonify({"error": "username e password são obrigatórios"}), 400

# Ver se já tem o login
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "username já existe"}), 400

# criptografar a senha em hash
    password_hash = bcrypt.hashpw(password.encode(
        "utf-8"), bcrypt.gensalt()).decode("utf-8")

# Salvar no banco
    user = User(username=username, password_hash=password_hash)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message:": "usuário criado", "id": user.id, "username": user.username}), 201


@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    password = (data.get("password") or "")

    if not username or not password:
        return jsonify({"error": "username e password obrigatórios"}), 400

# Compara usuario
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "credenciais invalidas"}), 401
# Compara senhas digitadas
    ok = bcrypt.checkpw(password.encode("utf-8"),
                        user.password_hash.encode("utf-8"))
    if not ok:
        return jsonify({"Error": "credenciais inválidas"}), 401

    token = create_access_token(identity=str(user.id))
    return jsonify({"access_token": token}), 200


@auth_bp.get("/me")
@jwt_required()
def me():
    user_id = get_jwt_identity()
    return jsonify({"user_id": user_id})
