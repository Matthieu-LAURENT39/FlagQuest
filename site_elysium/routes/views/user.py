from . import main
from flask import render_template, abort, redirect, url_for
from datetime import date, timedelta
from flask_login import current_user
from ...models import User
from ...utils import get_n_around

from pychartjs import BaseChart, ChartType, Color


class UserWeekPoints(BaseChart):
    """Graphe représentant les points d'un utilisateur sur 7 jours"""

    type = ChartType.Line

    class labels:
        """Les labels du graphe"""

        grouped = []

    class data:
        """Les données du graphe"""

        label = "Points"
        labels = []
        data = []
        backgroundColor = Color.Green


@main.route("/profile", defaults={"username": None})
@main.route("/profile/<username>")
def profile(username):
    """La page de profil de l'utilisateur"""

    if username is None:
        if current_user.is_authenticated:
            return redirect(url_for("main.profile", username=current_user.username))
        else:
            abort(401)
    else:
        user = User.query.filter_by(username=username).first_or_404(
            description="Cet utilisateur n'existe pas."
        )

    chart = UserWeekPoints()

    day_to_points: dict[str, int] = {}
    today = date.today()
    # For days from 6 day ago to today
    for offset in range(6, -1, -1):
        day = today - timedelta(days=offset)
        day_to_points[day.strftime("%d/%m/%Y")] = user.points_at_date(day)

    chart.labels.grouped = list(day_to_points.keys())
    chart.data.data = list(day_to_points.values())

    all_users = list(sorted(User.query.all(), key=lambda u: u.score, reverse=True))
    user_index = all_users.index(user)

    ranking_users = [
        (all_users.index(u) + 1, u)
        for u in get_n_around(lst=all_users, index=user_index, amount=5)
    ]

    return render_template(
        "profile.jinja",
        user=user,
        chart_json=chart.get(),
        ranking_users=ranking_users,
        user_position=user_index + 1,
    )


@main.route("/classement")
def classement():
    """Un classement de tout les utilisateurs"""

    # tri par ordre score : décroissant
    user = sorted(User.query.all(), key=lambda u: u.score, reverse=True)

    # compte nombre total d'utilisateurs
    nbr_user = User.query.count()
    return render_template("classement.jinja", user=user, nbr_user=nbr_user)
