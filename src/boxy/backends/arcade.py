from arcade.types import RGBOrA255
from .abstract import AbstractCrafter
from typing import Callable, Optional
from PIL import Image
import arcade
import logging
import re

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def _hex_to_rgb(hex_color: str) -> RGBOrA255:
    assert bool(re.fullmatch(r"#([0-9a-fA-F]{6}|[0-9a-fA-F]{8})", hex_color)), f"Bad color format for #RRGGBB/#RRGGBBAA: {hex_color}"

    hex_color = hex_color.lstrip("#")
    if len(hex_color) == 6:
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4)) #type: ignore
    elif len(hex_color) == 8:
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4, 6)) #type: ignore
    else:
        raise ValueError("Invalid hex color format")

class ArcadeCrafter(AbstractCrafter):
    def __init__(self, nb_lignes: int, nb_colonnes: int, cell_size: int, margin: int, init: Callable[[], None]):
        super().__init__(nb_lignes, nb_colonnes, cell_size, margin, init)
        WINDOW_WIDTH = (self.cell_size + self.margin) * self.ncols + self.margin
        WINDOW_HEIGHT = (self.cell_size + self.margin) * self.nrows + self.margin
        WINDOW_TITLE = ""

        self.window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
        self.view = GameView(self)



    def start(self, fn_click: Optional[Callable[[int, int], None]],
                    fn_key: Optional[Callable[[str], None]],
                    fn_draw: Optional[Callable[[], None]],
                    fn_update: Optional[Callable[[], None]]):
        """Cette fonction permet de démarrer l'affichage
        d'une grille de taille nb_lign x nb_colonnes.
        la fonction chargée de la gestion du clic est la fonction fn_click
        """
        super().start(fn_click, fn_key, fn_draw, fn_update)

        self.view.window.show_view(self.view)

        arcade.run()


    def set_fps(self, fps: int):
        super().set_fps(fps)
        self.window.set_update_rate(1/self.fps)


    def exit(self):
        pass


    def set_cell_color(self, i: int, j: int, couleur: str):
        """permet de colorier une case de la grille"""
        if i >= self.nrows or j >= self.ncols:
            return
        i = self.nrows - 1 - i

        # TODO improve by not recreating each time
        empty_image = Image.new("RGBA", (self.cell_size, self.cell_size), (255, 255, 255, 255))
        empty_texture = arcade.Texture(name="vide", image=empty_image)

        self.view.grid_sprites[i][j].texture = empty_texture
        self.view.grid_sprites[i][j].color = _hex_to_rgb(couleur)

    def set_cell_image(self, i: int, j: int, image: str):
        """Color cell i,j with image in cache"""
        if i >= self.nrows or j >= self.ncols:
            return
        i = self.nrows - 1 - i
        self.view.grid_sprites[i][j].color = _hex_to_rgb("#FFFFFFFF")
        self.view.grid_sprites[i][j].texture = self.view.textures[image]


    def set_cell_char(self, i: int, j: int, char: str, color: str):
        super().set_cell_char(i, j, char, color)
        if 0 <= i < self.nrows and 0 <= j < self.ncols:
            i_flipped = self.nrows - 1 - i
            sprite = self.view.grid_sprites[i_flipped][j]

            if char:
                # Create or update the Text
                if self.view.grid_chars[i][j] is None:
                    self.view.grid_chars[i][j] = arcade.Text(
                        text=char,
                        x=sprite.center_x,
                        y=sprite.center_y,
                        color=_hex_to_rgb(color),
                        font_size=48,
                        anchor_x="center",
                        anchor_y="center"
                    )
                elif self.view.grid_chars[i][j].text != char: #type: ignore
                    self.view.grid_chars[i][j].text = char #type: ignore
            else:
                # Clear the character
                self.view.grid_chars[i][j] = None

    def load_image(self, name: str, path: str):
        self.view.textures[name] = arcade.load_texture(path)
        self.view.textures[name].width = self.cell_size
        self.view.textures[name].height = self.cell_size


    def show_init_dialog(self, texte1: str, texte2: str):
        print("Not implemented yet")

    def play_sound(self, path: str):
        son = arcade.load_sound(path)
        son.play()



class GameView(arcade.View):
    """
    Main application class.
    """

    def __init__(self, crafter: ArcadeCrafter):
        """
        Set up the application.
        """
        super().__init__()
        self.crafter = crafter
        # Set the background color of the window
        self.background_color = arcade.color.BLACK

        self.textures: dict[str, arcade.Texture] = dict()
        # 1d list of all sprites in the two-dimensional sprite list
        self.grid_sprite_list: arcade.SpriteList[arcade.Sprite] = arcade.SpriteList()

        # 2d grid hat holds references to the spritelist
        self.grid_sprites: list[list[arcade.Sprite]] = []

        # 2d grid that holds Texts to be drawn on top of sprites
        self.grid_chars: list[list[arcade.Text|None]] = [[None for _ in range(crafter.ncols)] for _ in range(crafter.nrows)]

        # Create a list of solidcolor sprites to represent each cell
        for row in range(self.crafter.nrows):
            self.grid_sprites.append([])
            for column in range(self.crafter.ncols):
                x = column * (self.crafter.cell_size + self.crafter.margin) + (self.crafter.cell_size / 2 + self.crafter.margin)
                y = row * (self.crafter.cell_size + self.crafter.margin) + (self.crafter.cell_size / 2 + self.crafter.margin)
                sprite = arcade.SpriteSolidColor(self.crafter.cell_size, self.crafter.cell_size, color=arcade.color.WHITE)
                sprite.center_x = x
                sprite.center_y = y
                self.grid_sprite_list.append(sprite)
                self.grid_sprites[row].append(sprite)


    def on_update(self, delta_time: float) -> bool | None:
        logger.debug(f"on_update({delta_time})")
        #print("test")
        super().on_update(delta_time)
        if self.crafter.fn_update:
            self.crafter.fn_update()


    def on_key_press(self, symbol: int, modifiers: int) -> bool | None:
        logger.debug(f"on_key_press({symbol}, {modifiers})")
        super().on_key_press(symbol, modifiers)
        #print(symbol, chr(symbol), modifiers)
        if self.crafter.fn_key:
            self.crafter.fn_key(chr(symbol))
            self.immediate_update()


    def on_draw(self):
        """
        Render the screen.
        """
        if self.crafter.fn_draw:
            self.crafter.fn_draw()
        self.clear()
        self.grid_sprite_list.draw()
        #print(self.grid_chars)
        for i in range(self.crafter.nrows):
            for j in range(self.crafter.ncols):
                text_obj = self.grid_chars[i][j]
                if text_obj:
                    text_obj.draw()


    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        """
        Called when the user presses a mouse button.
        """
        logger.debug(f"on_mouse_press({x},{y},{button},{modifiers})")
        column = int(x // (self.crafter.cell_size + self.crafter.margin))
        row = self.crafter.nrows - 1 - int(y // (self.crafter.cell_size + self.crafter.margin))
        logger.debug(f"Grid coordinates: ({row}, {column})")
        if self.crafter.fn_click:
            self.crafter.fn_click(row, column)
            self.immediate_update()


    def immediate_update(self):
        self.on_update(0)
        self.window.set_update_rate(0)
        self.on_draw()
        self.window.flip()
        self.window.set_update_rate(1/self.crafter.fps)


class InformationView(arcade.View):

    def __init__(self, view: arcade.View, background_color: str) -> None:
        self.window = view.window
        self.view = view

        super().__init__(self.window, _hex_to_rgb(background_color) if background_color else None)


    def on_draw(self):
        self.clear()
        arcade.draw_text("Instructions Screen", self.window.width / 2, self.window.height / 2,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text("Click to advance", self.window.width / 2 , self.window.height / 2 - 75,
                         arcade.color.GRAY, font_size=20, anchor_x="center")

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        game_view = self.view
        self.window.show_view(game_view)
