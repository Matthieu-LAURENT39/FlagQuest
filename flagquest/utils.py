"""
Fonctions utilitaires pour tout le projet
"""

from itertools import count
from collections import deque
from typing import Iterator, TypeVar
import toml

T = TypeVar("T")


def get_n_around(lst: list[T], index: int, amount: int) -> list[T]:
    """Renvois les n éléments les plus proches de l'index "index", incluant
    l'élémént à la position index.

    Args:
        lst (list[T]): La liste contenant les éléments
        index (int): L'index servant de centre dans lst
        amount (int): Combient d'objets récupéré

    Raises:
        ValueError: amount est négatif, ou index n'est pas dans la liste

    Returns:
        list[T]: Une liste de "amount" éléments, ou de len(lst) si len(lst) < amount
    """

    # Sanity checks
    if amount < 0:
        raise ValueError("Amount can't be negative")
    if not 0 <= index < len(lst):
        raise ValueError("Index not in list")

    # * The list doesn't have enough elements, so we return it directly
    # * since it's the max amount we'll be able to return
    if len(lst) <= amount:
        return lst

    def neg_pos_count() -> Iterator[int]:
        """Yields growing ints, first the negative then the positive
        ex: 0, -1, -1, -2, 2, -3, ...

        Yields:
            Iterator[int]: An endless iterator of ints
        """
        yield 0
        for i in count(start=1):
            yield -i
            yield i

    # We use a deque since we'll add both to the start and the end
    output = deque()
    index_iterator = neg_pos_count()
    while len(output) < amount:
        target_index = index + next(index_iterator)
        # We don't want indexes outside the list
        if not 0 <= target_index < len(lst):
            continue

        # * We add to the start or the end, keeping the original list's order
        if target_index < index:
            output.appendleft(lst[target_index])
        else:
            output.append(lst[target_index])

    return list(output)


def add_room_from_toml(toml_txt: str) -> None:
    """Ajoute des questions a la base de donnée a partir de texte TOML

    Args:
        toml_txt (str): Le texte TOML a parse

    Raises:
        ValueError: La room est déja dans la base de données
    """
    from . import db
    from .models import Room, Question

    data = toml.loads(toml_txt)

    if Room.query.filter_by(url_name=data["url_name"]).first() is not None:
        raise ValueError("La room est déja dans la base de données")

    r = Room(
        name=data["name"],
        description=data["description"],
        url_name=data["url_name"],
        instructions=data["instructions"],
        victim_vm_ids=data["victim_vm_ids"],
    )
    db.session.add(r)
    # Pour que r obtienne un id
    db.session.flush()

    for q in data.get("question", []):
        db.session.add(
            Question(
                prompt=q["prompt"],
                answer=q["answer"],
                points=q["points"],
                room_id=r.id,
            )
        )

    db.session.commit()
