from flask_sqlalchemy import SQLAlchemy

from site_elysium.app import app

db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
db.init_app(app)
