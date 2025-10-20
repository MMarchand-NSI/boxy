import gridcrafter


"""
Refaire. Pourri.
"""


type coord = tuple[int, int]

class TicTacToe:
    def __init__(self, moteur: gridcrafter.AbstractCrafter) -> None:
        self.moteur = moteur
        self.reset()

    def reset(self):
        self.coups_joueurs: tuple[list[coord], list[coord]] = ([], [])
        self.joueur_courant = 1
        self.grille = [[0]*3 for _ in range(3)]


    def changer_joueur(self):
        self.joueur_courant = 5 - self.joueur_courant


    def peut_jouer(self, i: int, j: int) -> bool:
        return (i, j) not in self.coups_joueurs[0] + self.coups_joueurs[1]


    def jouer(self, i: int, j: int):
        if self.peut_jouer(i,j):
            self.grille[i][j] = self.joueur_courant
            j01=(self.joueur_courant - 1)//3
            self.coups_joueurs[j01].append((i,j))
            if len(self.coups_joueurs[j01]) > 3:
                old = self.coups_joueurs[j01].pop(0)
                self.grille[old[0]][old[1]] = 0
            if self.gagne():
                print("GAGNE")
            self.changer_joueur()


    def dessiner(self):
        for i in range(3):
            for j in range(3):
                tmp = self.grille[i][j]
                couleur = "#FFFFFF" if tmp == 0 else "#FF0000" if tmp == 1 else "#0000FF"
                self.moteur.set_cell_color(i,j,couleur)


    def gagne(self) -> bool:
        lignes = (self.grille + list(zip(*self.grille)) #lignes et colonnes
        + [[self.grille[i][i] for i in range(3)]]  #diag1
        + [[self.grille[i][2-i] for i in range(3)]]) # diag2

        return any(sum(ligne) == 3*self.joueur_courant for ligne in lignes)


if __name__ == "__main__":
    moteur = gridcrafter.create(3, 3, 100, 2, TicTacToe.reset)
    morpion = TicTacToe(moteur)
    moteur.start(fn_click=morpion.jouer, fn_key= None, fn_update= None, fn_draw = morpion.dessiner)
