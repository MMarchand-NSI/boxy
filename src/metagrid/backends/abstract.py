from typing import Callable
from abc import ABCMeta, abstractmethod

class AbstractEngine(metaclass = ABCMeta):
    """
    Abstracting the functionalities independently of its implementation
    """

    def __init__(self, nb_lignes: int, nb_colonnes: int, cell_size: int, margin: int) -> None:
        """
        Initialisation du jeu.
        """
        self.margin: int = margin        # grid line with (px)
        self.nrows: int = nb_lignes      # Number of rows
        self.ncols: int = nb_colonnes    # Number of columns
        self.cell_size: int = cell_size  # Cell size
        self.fps: int = 60               # FPS, defaults to 60
        self.frame_no: int = 0           # Holds the number of frame since start
        



    @abstractmethod
    def start(self, init: Callable[[], None],
                    fn_click: Callable[[int, int], None] | None,
                    fn_key: Callable[[str], None] | None,
                    fn_draw: Callable[[], None],
                    fn_update: Callable[[], None]) -> None:
        """
        Start the engine, declaring init function and callbacks.

        ### Parameters
        1. init
                - The function needed to initialize the state of the game
        2. fn_click
                - Callback handling the click on the cell (i, j)
        3. fn_key
                - Callback handling the key pressed
        4. fn_draw
                - Function that will be called for every frame to render graphics, right after update's call 
        5. fn_update
                - Function that will be called for every frame, right before draw's call
        """
        self.init: Callable[[], None] = init
        self.fn_click: Callable[[int, int], None] | None = fn_click
        self.fn_key: Callable[[str], None] | None= fn_key
        self.fn_draw: Callable[[], None] | None = fn_draw
        self.fn_update: Callable[[], None] | None = fn_update
        init()
        ...


    @abstractmethod
    def exit(self) -> None:
        """Exit the application"""
        ...

    @abstractmethod
    def set_cell_color(self, i: int, j: int, couleur: str) -> None:
        """Allows you to color a cell in the grid"""
        ...

    @abstractmethod
    def set_cell_image(self, i: int, j: int, image: str) -> None:
        """Allows you to display an image inside the cell of the grid.
        Use the name you gave the image when you loaded it using the function `load_image`
        """
        ...

    @abstractmethod
    def set_cell_char(self, i: int, j: int, char: str, color: str) -> None:
        """Prints a character at the given coordinates in the grid"""
        assert len(char) < 2
        ...


    @abstractmethod
    def load_image(self, name: str, path: str) -> None:
        """
        Loads the image stored at `path` under the `name` key in the engine's textures cache
        You have to load all the images at startup, giving them a name that you will use in the function `set_cell_image`.

        Example use:
        >>> images = ["angel", "demon", "key", "door"]
        >>> for nom in images:
        ...     engine.load_image(nom, f"assets/wordle/{nom}.png")

        """
        ...

    @abstractmethod
    def show_init_dialog(self, text1: str, text2: str) -> None:
        """Shows a screen with text1 and text2 right under.
        Click on the screen to dismiss it then run the init callback
        """
        ...

    @abstractmethod
    def play_sound(self, path: str) -> None:
        """
        Plays a sound file immediately when called, given its path. 
        """
        ...
