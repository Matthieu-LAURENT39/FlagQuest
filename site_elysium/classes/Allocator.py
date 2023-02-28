from itertools import cycle
from threading import Lock
from typing import Generic, Iterator, Optional, TypeVar

Resource = TypeVar("Resource")

# TODO: Rewrite using deque (https://docs.python.org/3/library/collections.html#collections.deque)
class Allocator(Generic[Resource]):
    """Gère l'allocations de ressources a partir d'une source."""

    def __init__(
        self, source: Iterator[Resource], allocated: Optional[set[Resource]] = None
    ) -> None:
        """Créer l'alloueur de ressources.

        Args:
            source (Iterator[Resource]): L'entiereté des resources allouable.
            allocated (Optional[set[Resource]], optional): Les resources qui sont déja alloué. Defaults to None.
        """
        self.source = cycle(source)
        if allocated is None:
            allocated = set()
        self._allocated = allocated
        self._lock = Lock()

    def allocate(self) -> Resource:
        """Alloue une ressource libre. Thread-safe.

        Returns:
            Resource: La ressource alloué.
        """
        first_tried = None
        with self._lock:
            while (resource := next(self.source)) in self._allocated:
                if first_tried is None:
                    first_tried = resource
                else:
                    # Cela veut dire que l'on a fait le tour de l'itérateur.
                    if first_tried == resource:
                        raise ValueError("Plus de resources à allouer!")
            self._allocated.add(resource)
        return resource

    def free(self, resource: Resource) -> None:
        """Libére une ressource qui avait été alloué précédement. Thread-safe.

        Args:
            resource (Resource): La ressource à libéré.
        """
        with self._lock:
            try:
                self._allocated.remove(resource)
            except KeyError as e:
                raise ValueError(
                    "Cette resource n'est pas alloué et ne peut donc pas être libéré."
                ) from e
