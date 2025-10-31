from typing import Callable
from abc import ABCMeta, abstractmethod

class AbstractCrafter(metaclass = ABCMeta):
    """
    Abstracting the functionalities independently of its implementation
    """

    def __init__(self, nb_lignes: int, nb_colonnes: int, cell_size: int, margin: int, init: Callable[[], None]):
        """
        Initialisation du jeu.
        """
        self.margin: int = margin        # grid line with (px)
        self.nrows: int = nb_lignes      # Number of rows
        self.ncols: int = nb_colonnes    # Number of columns
        self.cell_size: int = cell_size  # Cell size
        self.fps: int = 60               # FPS, defaults to 60
        self.frame_no: int = 0           # Holds the number of frame since start
        self.init: Callable[[], None] = init



    @abstractmethod
    def start(self, fn_click: Callable[[int, int], None] | None,
                    fn_key: Callable[[str], None] | None,
                    fn_draw: Callable[[], None],
                    fn_update: Callable[[], None]):
        """
        Start the engine, declaring callbacks
        """
        self.fn_click: Callable[[int, int], None] | None = fn_click
        self.fn_key: Callable[[str], None] | None= fn_key
        self.fn_draw: Callable[[], None] | None = fn_draw
        self.fn_update: Callable[[], None] | None = fn_update
        ...


    @abstractmethod
    def exit(self):
        """Permet de fermer l'application"""
        ...

    @abstractmethod
    def set_cell_color(self, i: int, j: int, couleur: str):
        """permet decolorier une case de la grille"""
        ...

    @abstractmethod
    def set_cell_image(self, i: int, j: int, image: str):
        """permet decolorier une case de la grille"""
        ...

    @abstractmethod
    def set_cell_char(self, i: int, j: int, char: str, color: str):
        """sets a cell to a character"""
        assert len(char) < 2
        ...


    @abstractmethod
    def load_image(self, name: str, path: str):
        """Loads the image stored at `path` under the `name` key in the engine's textures cache"""
        ...

    @abstractmethod
    def show_init_dialog(self, texte1: str, texte2: str):
        """shows a screen with text1 and text2 right under.
        Click on the screen to dismiss it then run the init callback"""
        ...

    @abstractmethod
    def play_sound(self, path: str):
        ...
