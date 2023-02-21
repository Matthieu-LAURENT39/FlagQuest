import mimetypes
from site_elysium.app import app
import site_elysium.backend
from site_elysium.models import User, Room, Question
from werkzeug.security import generate_password_hash


mimetypes.add_type("application/javascript", ".js")

with app.app_context():
    site_elysium.backend.db.create_all()

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
        site_elysium.backend.db.session.add(user)
        site_elysium.backend.db.session.commit()

    room = Room.query.filter_by(id="1").first()
    if room is None:
        room = Room(
            name="Room 1",
            description="Wow what a cool room **desu wa**",
            url_name="room1",
            instructions="QCM",
            victim_vm_ids=[100],
        )
        room2 = Room(
            name="Room 2",
            description="lorem ipsum dolor sit amet",
            url_name="room2",
            instructions="QCM",
        )
        room3 = Room(
            name="Room 3",
            description="lorem ipsum dolor sit amet",
            url_name="room3",
            instructions="QCM",
        )
        room4 = Room(
            name="Room 4",
            description="lorem ipsum dolor sit amet",
            url_name="room4",
            instructions="QCM",
        )
        room5 = Room(
            name="Room 5",
            description="lorem ipsum dolor sit amet",
            url_name="room5",
            instructions="QCM",
        )
        room6 = Room(
            name="Room 6",
            description="lorem ipsum dolor sit amet",
            url_name="room6",
            instructions="QCM",
        )

        site_elysium.backend.db.session.add(room)
        site_elysium.backend.db.session.add(room2)
        site_elysium.backend.db.session.add(room3)
        site_elysium.backend.db.session.add(room4)
        site_elysium.backend.db.session.add(room5)
        site_elysium.backend.db.session.add(room6)

        site_elysium.backend.db.session.commit()

        # room.users.append(user)
        # backend.db.session.commit()

    question = Question.query.filter_by(id="1").first()
    if question is None:
        for i in range(6):
            question = Question(room_id=1, prompt=f"{i}+1=?", answer=str(i + 1))
            site_elysium.backend.db.session.add(question)
            site_elysium.backend.db.session.commit()

if __name__ == "__main__":
    app.run("0.0.0.0", 5000, debug=True)
