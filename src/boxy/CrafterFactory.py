from typing import Literal, Callable

from . import backends

BackendName = Literal["arcade"]

class CrafterFactory:

    @staticmethod
    def create(backend: BackendName, nrows: int,
            ncols: int, cell_size: int, margin: int, init: Callable[[], None]) -> backends.AbstractCrafter:
        """
        Crée une instance de moteur de grille selon le backend choisi.

        Retourne une instance du crafter choisi (ArcadeCrafter est le seul backend supporté pour l'instant).
        """
        if backend == "arcade":
            from .backends.arcade import ArcadeCrafter
            return ArcadeCrafter(nrows, ncols, cell_size, margin, init)
        else:
            raise ValueError(f"Backend inconnu : {backend!r}")
