try:
    from importlib.metadata import version
    __version__ = version("boxy")
except Exception:
    __version__ = "0.0.0"


from .backends import AbstractCrafter
from .CrafterFactory import CrafterFactory
from typing import Callable

def create(nb_lignes: int, nb_colonnes: int, cell_size: int, margin: int, init: Callable[[], None]) -> AbstractCrafter:
    return CrafterFactory.create("arcade", nb_lignes, nb_colonnes, cell_size, margin, init)

__all__ = ["create"]
