import metagrid

grille: list[list[int]] = [
    [0, 1, 0, 0, 0],
    [0, 0, 2, 1, 0],
    [2, 0, 0, 0, 3],
    [0, 1, 0, 0, 3],
    [0, 0, 0, 0, 1],
]

def init():
    print("Jeu initialisé")


def touche(key: str):
    print(f"Touche {key} enfoncée")


def clique(i: int, j: int):
    print(f"Case ({i}, {j}) cliquée")

def update():
    global game
    if game.frame_no % 120 == 0:
        print("Update quand le numéro de frame est un multiple de 120")

def draw():
    global game
    for i in range(5):
        for j in range(5):
            val = grille[i][j]
            if val == 1:
                game.set_cell_color(i, j, "#135683")
            elif val == 2:
                game.set_cell_char(i, j, "X", "#000000")


if __name__ == "__main__":
    game = metagrid.create(5, 5, 50, 1)
    game.start(init, fn_click=clique, fn_key=touche, fn_update=update, fn_draw=draw)



