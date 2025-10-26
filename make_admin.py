from app import app
from models import db, User

with app.app_context():
    user = User.query.filter_by(email="luisa1234@gmail.com").first()
    if user:
        user.is_admin = True
        db.session.commit()
        print("Usuario convertido en administrador.")
    else:
        print("Usuario no encontrado.")