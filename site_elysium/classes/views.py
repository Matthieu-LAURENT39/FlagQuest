from flask import abort, flash, redirect, render_template, url_for
from flask_admin import AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user


class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin == True


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
