try:
    from importlib.metadata import version
    __version__ = version("easygrid")
except Exception:
    __version__ = "0.0.0"


from typing import Callable
from .backends import AbstractCrafter
from .CrafterFactory import CrafterFactory

def create(nb_lignes: int, nb_colonnes: int, cell_size: int, margin: int, init: Callable[[], None]) -> AbstractCrafter:
    return CrafterFactory.create("arcade", nb_lignes, nb_colonnes, cell_size, margin, init)

__all__ = ["create"]
