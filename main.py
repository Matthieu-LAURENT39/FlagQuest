import mimetypes
from app import app
import backend

mimetypes.add_type("application/javascript", ".js")

with app.app_context():
    backend.db.create_all()

app.run("0.0.0.0", 8080, debug=True)
