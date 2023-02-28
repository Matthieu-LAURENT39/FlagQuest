import wtforms
from flask_wtf import FlaskForm


class SignupForm(FlaskForm):
    """Formulaire de connexion"""

    username = wtforms.StringField(
        "Votre pseudo", validators=[wtforms.validators.DataRequired()]
    )
    email = wtforms.EmailField(
        "Votre adresse email", validators=[wtforms.validators.DataRequired()]
    )
    password = wtforms.PasswordField(
        "Votre mot de passe", validators=[wtforms.validators.DataRequired()]
    )
    password_confirmation = wtforms.PasswordField(
        label="Password confirm",
        validators=[
            wtforms.validators.DataRequired(),
            wtforms.validators.EqualTo(
                "password", message="Les mots de passe doivent être identique."
            ),
        ],
    )
    submit = wtforms.SubmitField("Valider")
