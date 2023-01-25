import mimetypes
from app import app
import backend
from models import User, Room, Question
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
            score=12,
        )
        backend.db.session.add(user)
        backend.db.session.commit()

    room = Room.query.filter_by(id="1").first()
    if room is None:
        room = Room(
            name="Room 1",
            description="Wow what a cool room",
            url_name="room1",
            instructions="Lorem **ipsum** dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex",
        )
        room2 = Room(
            name="Room 2",
            description="lorem ipsum dolor sit amet",
            url_name="room2",
            instructions="a",
        )
        backend.db.session.add(room)
        backend.db.session.add(room2)

        backend.db.session.commit()

        # room.users.append(user)
        # backend.db.session.commit()

    question = Question.query.filter_by(id="1").first()
    if question is None:
        question = Question(room_id=1, prompt="1+1=?", answer="2")
        backend.db.session.add(question)
        backend.db.session.commit()

if __name__ == "__main__":
    app.run("0.0.0.0", 5000, debug=True)
