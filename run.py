from app import create_app
from app.extensions import db
from app.models import User

# Aplicação Flask

app = create_app()

if __name__ == '__main__':
    # criar banco de dados quando rodar
    with app.app_context():
        db.create_all()

    # Inicia o servidor
    app.run(host="127.0.0.1", port=5000, debug=True)
