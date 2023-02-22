from markdown import markdown as md


def markdown_filter(text: str) -> str:
    """Interprète le markdown vers de l'HTML

    Args:
        text (str): Texte contenant du markdown

    Returns:
        str: HTML de ce texte.
    """
    return md(text)
