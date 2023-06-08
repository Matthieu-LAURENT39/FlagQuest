"""
Formulaire WTForms pour l'inscription
"""

from flask_wtf import FlaskForm
import wtforms


class SignupForm(FlaskForm):
    """Formulaire d'inscription"""

    username = wtforms.StringField(
        "Votre pseudo",
        validators=[
            wtforms.validators.DataRequired(),
            wtforms.validators.Length(
                max=30,
                message="Le nom d'utilisateur doit faire moins de 30 charactères.",
            ),
        ],
    )
    """Le nom d'utilisateur"""
    email = wtforms.EmailField(
        "Votre adresse email", validators=[wtforms.validators.DataRequired()]
    )
    """L'adresse email"""
    password = wtforms.PasswordField(
        "Votre mot de passe", validators=[wtforms.validators.DataRequired()]
    )
    """Le mot de passe"""
    password_confirmation = wtforms.PasswordField(
        label="Confirmation du mot de passe",
        validators=[
            wtforms.validators.DataRequired(),
            wtforms.validators.EqualTo(
                "password", message="Les mots de passe doivent être identique."
            ),
        ],
    )
    """La confirmation du mot de passe"""
    submit = wtforms.SubmitField("Valider")
    """Le bouton pour envoyer le formulaire"""
