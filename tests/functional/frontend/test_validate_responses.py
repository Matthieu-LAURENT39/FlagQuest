"""
Vérifie que le code HTML généré par les templates est de l'HTML5 valide.
"""

from flask import Flask, url_for
from flask.testing import FlaskClient

# TODO: Réécrire ce test

# // def _validate_HTML(html: str) -> bool:
# //     """Valide que l'HTML est valide.

# //     Args:
# //         html (str): L'HTML à valider.

# //     Returns:
# //         bool: True si l'HTML est valide, sinon Faux.
# //     """

# //     html5lib.parse(html)


# // def test_validate_routes(app: Flask, client: FlaskClient):
# //     app.url_map
# //     r = client.get(url_for("main.acceuil"))
# //     if "text/html" in r.content_type:
# //         html = r.data.decode(r.charset)
# //         html = "<html><tail"
# //         _validate_HTML(html)
