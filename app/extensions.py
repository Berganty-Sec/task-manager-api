from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

#Papo do banco de dados
db = SQLAlchemy()

#Autenticação JWT
jwt = JWTManager()