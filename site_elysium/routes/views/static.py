from flask import send_file

from . import main
from ...models import User
from io import BytesIO


@main.route("/profile_picture/<username>.png")
def profile_picture(username):
    """A 250x250 profile picture"""
    user: User = User.query.filter_by(username=username).first_or_404(
        description="Cet utilisateur n'existe pas."
    )

    return send_file(
        BytesIO(user.get_profile_picture(size=250)),
        download_name=f"{username}.png",
        mimetype="image/png",
    )
