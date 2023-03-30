from site_elysium.utils import get_n_around
import pytest


@pytest.mark.parametrize(
    "lst,index,amount,expected",
    [
        ([1, 2, 3, 4, 5], 0, 3, [1, 2, 3]),
        ([1, 2, 3, 4, 5], 4, 3, [3, 4, 5]),
        ([5, 4, 3, 2, 1], 2, 3, [4, 3, 2]),
        ([1, 2, 3], 1, 500, [1, 2, 3]),
        ([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 1, 5, [0, 1, 2, 3, 4, 5]),
        ([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 2, 5, [0, 1, 2, 3, 4, 5]),
        ([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 6, 5, [4, 5, 6, 7, 8]),
    ],
)
def test_get_n_around(lst, index, amount, expected):
    """
    Teste que get_n_around renvois bien les bonnes valeurs
    """


def test_get_n_around_errors():
    """
    Teste que get_n_around n'accepte pas de mauvais paramètres
    """
    lst = [1, 2, 3, 4, 5]

    # On vérifie que des valeurs incorrectes
    with pytest.raises(ValueError):
        get_n_around(lst, 122, 2)

    with pytest.raises(ValueError):
        get_n_around(lst, -2, 2)

    with pytest.raises(ValueError):
        get_n_around(lst, 1, -5)
