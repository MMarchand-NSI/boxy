try:
    from importlib.metadata import version
    __version__ = version("metagrid")
except Exception:
    __version__ = "0.0.0"


from .backends import AbstractEngine
from .CrafterFactory import CrafterFactory

def create(nb_lignes: int, nb_colonnes: int, cell_size: int, margin: int) -> AbstractEngine:
    return CrafterFactory.create("arcade", nb_lignes, nb_colonnes, cell_size, margin)

__all__ = ["create", "AbstractEngine"]
