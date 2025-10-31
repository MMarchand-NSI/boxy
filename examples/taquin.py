import metagrid
from random import choice, randint


NB_LIGNES = 4
NB_COLONNES = NB_LIGNES
TAILLE_CASE = 128

grille: list[list[int]] # grille comportant le numero des tiles
itrou: int              # indice ligne du trou
jtrou: int              # indice colonne du trou

def init():
    """
    Initialisationn des variables du jeu.
    Il suffit d'appeler cette procédure pour réinitialiser le jeu.
    """
    global grille, itrou, jtrou
    (itrou, jtrou) = (0, 3) # Dans l'exemple, le trou est à (0, 3). Exemple de déconstruction de tuple
    grille = [[i * NB_COLONNES + j for j in range(TAILLE_CASE)] for i in range(NB_LIGNES)]
    melanger(100)



def melanger(n: int):
    """
    Répète n fois:
    - faire bouger aléatoirement en haut, en bas, à gauche, ou à droite.
    """
    global grille, itrou, jtrou
    for _ in range(n):
        if randint(0,1):
            bouge(itrou, jtrou+choice((-1,1)))
        else:
            bouge(itrou+choice((-1,1)), jtrou)


def gagne() -> bool:
    """
    si toutes les cases sont ordonnées, on a gagné
    """
    global grille
    return all(grille[i][j] == i * NB_COLONNES + j for i in range(NB_LIGNES) for j in range(NB_COLONNES))



def affiche_grille():
    """
    Méthode d'affichage du jeu
    """
    global grille, itrou, jtrou
    for i in range(NB_LIGNES):
        for j in range(NB_COLONNES):
            if grille[i][j] != grille[itrou][jtrou]:
                jeu.set_cell_image(i, j, f"tile{grille[i][j]}")
            else:
                jeu.set_cell_color(i, j, "#FFFFFF")


def bouge(i: int, j: int):
    """
    Bouge la case (i,j) dans le trou
    Si le trou est bien autour de i et de j: le trou et (i, j) sont intervertis
    """
    global grille, itrou, jtrou
    if not ( 0<=i<NB_LIGNES and 0<=j<NB_COLONNES):
        return
    if ((itrou==i) and jtrou in (j-1, j+1)) or ((jtrou==j) and itrou in (i-1, i+1)):
        trou = grille[itrou][jtrou]
        grille[itrou][jtrou] = grille[i][j]
        grille[i][j] = trou
        itrou, jtrou = i, j

    if gagne():
        print("GAGNE")
        # Afficher écran de fin

def update():
    pass

if __name__=="__main__":

    # Initialisation des variables du jeu
    init()

    # Initialisation du moteur
    jeu = metagrid.create(NB_LIGNES, NB_COLONNES, TAILLE_CASE, 0)

    # Chargement de toutes les images dans le moteur
    for i in range(16):
        jeu.load_image(f"tile{i}", f"assets/taquin/tile_{i}.png")

    # Lancement du moteur avec ses callbacks
    jeu.start(init, fn_draw=affiche_grille, fn_click=bouge, fn_key=None, fn_update=update)
