import wtforms
from flask_wtf import FlaskForm


class LoginForm(FlaskForm):
    """Formulaire de connexion"""

    login = wtforms.StringField(
        "Login ou adresse email", validators=[wtforms.validators.DataRequired()]
    )
    password = wtforms.PasswordField(
        "Mot de passe", validators=[wtforms.validators.DataRequired()]
    )
    submit = wtforms.SubmitField("Valider")
