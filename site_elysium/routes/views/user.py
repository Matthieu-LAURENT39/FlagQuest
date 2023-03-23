from . import main
from flask import render_template, abort, redirect, url_for
from datetime import date, timedelta
from flask_login import login_required, current_user, user_logged_in
from ...models import User

from pychartjs import BaseChart, ChartType, Color


class UserWeekPoints(BaseChart):
    type = ChartType.Line

    class labels:
        grouped = []

    class data:
        label = "Points over time"
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

    def get_index_or_none(lst: list, index: int):
        if index < 0:
            return None
        try:
            return (index + 1, lst[index])
        except IndexError:
            return None

    # We find the 2 users on each side around the user
    ranking_users = []
    # User is first
    if user_index == 1:
        ranking_users = [
            get_index_or_none(all_users, user_index),
            get_index_or_none(all_users, user_index + 1),
            get_index_or_none(all_users, user_index + 2),
        ]
    # User is last
    elif user_index == len(all_users) - 1:
        ranking_users = [
            get_index_or_none(all_users, user_index - 2),
            get_index_or_none(all_users, user_index - 1),
            get_index_or_none(all_users, user_index),
        ]
    else:
        ranking_users = [
            get_index_or_none(all_users, user_index - 1),
            get_index_or_none(all_users, user_index),
            get_index_or_none(all_users, user_index + 1),
        ]
    # We remove the Nones
    ranking_users = [u for u in ranking_users if u is not None]

    return render_template(
        "profile.jinja", user=user, chart_json=chart.get(), ranking_users=ranking_users
    )


@main.route("/classement")
def classement():
    """Un classement de tout les utilisateurs"""
    from ...models import User

    # tri par ordre score : décroissant
    user = sorted(User.query.all(), key=lambda u: u.score, reverse=True)

    # compte nombre total d'utilisateurs
    nbr_user = User.query.count()
    return render_template("classement.jinja", user=user, nbr_user=nbr_user)
