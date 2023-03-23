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

    return render_template("profile.jinja", user=user, chart_json=chart.get())


@main.route("/classement")
def classement():
    """Un classement de tout les utilisateurs"""
    from ...models import User

    # tri par ordre score : décroissant
    user = sorted(User.query.all(), key=lambda u: u.score, reverse=True)

    # compte nombre total d'utilisateurs
    nbr_user = User.query.count()
    return render_template("classement.jinja", user=user, nbr_user=nbr_user)
