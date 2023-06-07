"""
Filtres Jinja
"""

from markdown import markdown as md
from markdown.extensions.codehilite import CodeHiliteExtension
from bs4 import BeautifulSoup


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
    # - extra: permet l'utilisation de tableaux et de footnotes
    # - markdown_mark: permet de surligner du texte avec ==text==
    # - pymdownx.tasklist: permet l'utilisation de tasklists (style github)
    # - pymdownx.tilde: permet de barré du texte et d'utilisé du subscript
    md_html = md(
        text,
        extensions=[
            "fenced_code",
            "nl2br",
            CodeHiliteExtension(guess_lang=True, linenums=None),
            "extra",
            "markdown_mark",
            "pymdownx.tasklist",
            "pymdownx.tilde",
        ],
    )

    # Add bootstrap classes to prettify output
    soup = BeautifulSoup(md_html, "html.parser")

    # Find all table elements and add the "table" class
    tables = soup.find_all("table")
    for table in tables:
        table["class"] = table.get("class", []) + ["table"]

    # Find all blockquote elements and add the "blockquote" class
    tables = soup.find_all("blockquote")
    for table in tables:
        table["class"] = table.get("class", []) + ["blockquote"]

    # Return the modified HTML
    return soup.prettify()
