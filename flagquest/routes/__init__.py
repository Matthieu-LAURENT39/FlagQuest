"""
Routes Flask
"""

from flask import Blueprint

main = Blueprint("main", __name__)
api = Blueprint(
    "api",
    __name__,
    url_prefix="/api",
)

# flake8: noqa: E402
from . import views, _api
