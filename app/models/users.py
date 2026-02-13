from app.extensions import db
from datetime import datetime  # Data e hora

# Com isso crio a tabela de pra controle
# Com usuario, senha em hash e o horario e data


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)  # Coluna do ID
    # Coluna do Usuario, max. 80 caracteres
    username = db.Column(db.String(80), unique=True, nullable=False)
    # Coluna da senha em HASH, max. 255 caracteres
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow)  # Hora da criação
