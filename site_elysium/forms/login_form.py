from flask_wtf import FlaskForm
import wtforms


class LoginForm(FlaskForm):
    """Formulaire de connexion"""

    login = wtforms.StringField(
        "Nom d'utilisateur", validators=[wtforms.validators.DataRequired()]
    )
    """Le nom d'utilisateur de l'utilisateur"""
    password = wtforms.PasswordField(
        "Mot de passe", validators=[wtforms.validators.DataRequired()]
    )
    """Le mot de passe de l'utilisateur"""
    submit = wtforms.SubmitField("Valider")
    """Le bouton pour envoyer le formulaire"""
