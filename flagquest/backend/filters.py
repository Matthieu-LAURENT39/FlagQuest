"""
Filtres Jinja
"""

from markdown import markdown as md
from markdown.extensions.codehilite import CodeHiliteExtension


def markdown_filter(text: str) -> str:
    """Interprète le markdown vers de l'HTML

    Args:
        text (str): Texte contenant du markdown

    Returns:
        str: HTML de ce texte.
    """

    # Extensions utilisé:
    # - fenced_code: permet l'utilisation de code block avec ```
    # - nl2br: remplace \n par <br>
    # - CodeHiliteExtension: permet le synthax highlighting dans les code blocks
    # - tables: permet l'utilisation de tableaux
    return md(
        text,
        extensions=[
            "fenced_code",
            "nl2br",
            CodeHiliteExtension(guess_lang=True, linenums=None),
            "tables",
        ],
    )
