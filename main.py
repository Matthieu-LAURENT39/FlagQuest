import mimetypes
from app import app
import backend
from database import User
from werkzeug.security import generate_password_hash

mimetypes.add_type("application/javascript", ".js")

with app.app_context():
    backend.db.create_all()

with app.app_context():
    user = User.query.filter_by(username="admin").first()
    if user is None:
        user = User(
            username="admin",
            email="feur@desu.wa",
            password_hash=generate_password_hash("admin"),
            is_admin=True,
        )
        backend.db.session.add(user)
        backend.db.session.commit()

if __name__ == "__main__":
    app.run("0.0.0.0", 5000, debug=True)
