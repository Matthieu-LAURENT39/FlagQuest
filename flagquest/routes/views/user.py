"""
Endpoints lié au profil de l'utilisateur
"""

from . import main
from flask import render_template, abort, redirect, url_for
from datetime import date, timedelta
from flask_login import current_user
from ...models import User, Room
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
def profile(username: str | None):
    """La page de profil de l'utilisateur"""

    # si on spécifie pas d'username dans l'URL, renvoyer celle de l'user connecté
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

    # progression room dans profile
    user_rooms = list(user.joined_rooms)
    for r in user_rooms:
        nbr_question_solved = sum(q.is_solved_by(user) for q in r.questions)

    return render_template(
        "profile.jinja",
        user=user,
        chart_json=chart.get(),
        ranking_users=ranking_users,
        user_position=user_index + 1,
        user_rooms=list(user.joined_rooms),
        nbr=nbr_question_solved,
    )


@main.route("/classement")
def classement():
    """Un classement de tout les utilisateurs"""

    # tri par ordre score : décroissant
    user = sorted(User.query.all(), key=lambda u: u.score, reverse=True)

    # compte nombre total d'utilisateurs
    nbr_user = User.query.count()

    return render_template("classement.jinja", user=user, nbr_user=nbr_user)
