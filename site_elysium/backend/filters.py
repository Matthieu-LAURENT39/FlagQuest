from site_elysium.app import app
from markdown import markdown as md


@app.template_filter()
def markdown(text: str) -> str:
    """Interprète le markdown vers de l'HTML

    Args:
        text (str): Texte contenant du markdown

    Returns:
        str: HTML de ce texte.
    """
    return md(text)
