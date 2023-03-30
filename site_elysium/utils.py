from itertools import count
from typing import Iterator, TypeVar


T = TypeVar("T")


def get_n_around(lst: list[T], index: int, amount: int) -> list[T]:
    """Renvois les n éléments les plus proches de l'index "index", incluant
    l'élémént à index.

    Args:
        lst (list[T]): La liste contenant les éléments
        index (int): L'index servant de centre dans lst
        amount (int): Combient d'objets récupéré

    Raises:
        ValueError: amount étais négatif, ou index n'étais pas dans la liste

    Returns:
        list[T]: Une liste de "amount" éléments, ou de la len(lst) si len(lst) < amount
    """

    # Sanity checks
    if amount < 0:
        raise ValueError("Amount can't be negative")
    if not 0 <= index < len(lst):
        raise ValueError("Index not in list")

    # The list doesn't have enough elements, so we return it directly
    # since it's the max amount we'll be able to return
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

    output_lst = []
    index_iterator = neg_pos_count()
    while len(output_lst) < amount:
        target_index = index + next(index_iterator)
        # We don't want indexes outside the list
        if target_index < 0 or target_index <= len(output_lst):
            continue
        output_lst.append(lst[target_index])

    return output_lst
