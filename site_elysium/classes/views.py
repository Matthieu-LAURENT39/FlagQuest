from flask_login import current_user
from flask_admin.contrib.sqla import ModelView


class AdminModelView(ModelView):
    """
    Une vue de modèle pour Flask-Admin.
    Accessible uniquement par les admins.
    """

    def is_accessible(self):
        """Vérifie que l'utilisateur a le droit d'accéder à la page"""
        return current_user.is_authenticated and current_user.is_admin


# class MyAdminIndexView(AdminIndexView):
#     @expose("/")
#     def index(self):
#         # si l'user n'est pas connecté -> error
#         if not current_user.is_authenticated:
#             abort(403)
#         # si l'user est admin -> interface admin
#         if current_user.is_admin == True:
#             return super(MyAdminIndexView, self).index()
#         else:
#             abort(403)
