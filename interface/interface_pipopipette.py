from tkinter import Tk, Frame, Button, Canvas, messagebox
from pipopipette.partie import PartiePipopipette
import os
import sys

class CanvasPipopipette(Canvas):
    # Dans le TP, vous devrez ajouter un argument planche en entrée
    # à ce constructeur.

    def __init__(self, planche, longueur_ligne=200):
        # Nombre de pixels par case, variable.
        self.planche = planche
        self.longueur_ligne = longueur_ligne
        self.largeur_ligne = self.longueur_ligne / 10
        self.dimension_boite = self.longueur_ligne + self.largeur_ligne

        # Dans le TP, ces champs devront être remplis à partir de l'attribut planche d'un objet Partie que vous ajouterez
        # au __init__(). Vous devrez aussi ajouter un attribut self.planche.
        #
        # Ici on crée des attributs n_boites_v, n_boites_h, lignes et boites, mais dans le TP
        # on lira directement ces attributs à partir de self.planche. Ces attributs sont donc
        # seulement pour les biens du labo, mais seront tous remplacés par self.planche dans le TP.
        self.planche.N_BOITES_V = 3
        self.planche.N_BOITES_H = 3

        super().__init__(
                         width=self.planche.N_BOITES_V * self.dimension_boite + self.largeur_ligne - 1,
                         height=self.planche.N_BOITES_H * self.dimension_boite + self.largeur_ligne - 1)

    def dessiner_boites(self):
        # Ici, on itère sur le dictionnaire self.boites, sans se servir de la valeur de boite.
        # Dans le TP, on itèrera sur self.planche.boites.items() et boite sera un objet de
        # type Boite.
        for position, boite in self.planche.boites.items():
            ligne, col = position

            # On retrouve les points d'ancrage en x et en y de la boîte à partir de sa ligne et de sa colonne
            debut_boite_x = col * self.dimension_boite + self.largeur_ligne
            debut_boite_y = ligne * self.dimension_boite + self.largeur_ligne
            fin_boite_x = debut_boite_x + self.longueur_ligne
            fin_boite_y = debut_boite_y + self.longueur_ligne

            # Ici, on crée des rectangles de couleur 'grey'. Dans votre TP, vous voudrez utiliser l'attribut
            # couleur de votre boite, c'est-à-dire utiliser 'fill=boite.couleur_affichage()'.
            self.create_rectangle(debut_boite_x, debut_boite_y, fin_boite_x, fin_boite_y, tags='boite', fill=boite.couleur_affichage())

    def dessiner_lignes(self):
        # Ici, on itère sur le dictionnaire self.lignes, sans se servir de la valeur de ligne.
        # Dans le TP, on itèrera sur self.planche.lignes.items() et ligne sera un objet de type
        # Ligne.
        for cle, ligne in self.planche.lignes.items():
            ligne_point, col_point, orientation = cle

            # On retrouve les points d'ancrage en x et en y de la ligne à partir de sa ligne, de sa colonne
            # et de son orientation
            if orientation == 'H':
                debut_ligne_x = col_point * self.dimension_boite + self.largeur_ligne
                debut_ligne_y = ligne_point * self.dimension_boite
                fin_ligne_x = debut_ligne_x + self.longueur_ligne
                fin_ligne_y = debut_ligne_y + self.largeur_ligne
            else:
                debut_ligne_x = col_point * self.dimension_boite
                debut_ligne_y = ligne_point * self.dimension_boite + self.largeur_ligne
                fin_ligne_x = debut_ligne_x + self.largeur_ligne
                fin_ligne_y = debut_ligne_y + self.longueur_ligne

            # Ici, on crée des rectangles de couleur 'white'. Dans votre TP, vous voudrez utiliser l'attribut
            # couleur de votre ligne, c'est-à-dire utiliser 'fill=ligne.couleur_affichage()'.
            self.create_rectangle(debut_ligne_x,
                                  debut_ligne_y,
                                  fin_ligne_x,
                                  fin_ligne_y,
                                  tags='ligne',
                                  fill=ligne.couleur_affichage(),
                                  width=1)

    def dessiner_points(self):
        # Cette fonction crée tous les points requis à partir des attributs self.n_boites_v et self.n_boites_h.
        # Dans le TP, on lira respectivement self.planche.N_BOITES_V et self.planche.N_BOITES_H
        for col in range(self.planche.N_BOITES_V + 1):
            for ligne in range(self.planche.N_BOITES_H + 1):
                origine_cercle_x = col * self.dimension_boite
                origine_cercle_y = ligne * self.dimension_boite
                fin_cercle_x = origine_cercle_x + self.largeur_ligne
                fin_cercle_y = origine_cercle_y + self.largeur_ligne

                self.create_rectangle(origine_cercle_x,
                                 origine_cercle_y,
                                 fin_cercle_x,
                                 fin_cercle_y,
                                 tags='point',
                                 fill='yellow')


    def obtenir_coup_joue(self, event):
        '''
        Méthode qui retrouve si un clic est fait sur une ligne, une boîte ou sur un point, et surtout pour retrouver
        laquelle.

        Dans votre TP, vous pourrez vous débarasser des sections de code concernant les clics sur un
        point et sur une boîte pour conserver seulement les sections sur les lignes et retourner None
        quand le clic est sur un point ou une boîte.

        Args:
            event (Event): L'objet Event relié au clic fait sur le canvas

        Returns:
            None si le clic a été fait sur un point, (int, int, orientation) s'il
            a été fait sur une ligne et (int, int, 'Boite') si c'était une boîte
        '''
        col = int(event.x // self.dimension_boite)
        ligne = int(event.y // self.dimension_boite)

        x_relatif = event.x % self.dimension_boite
        y_relatif = event.y % self.dimension_boite

        coup = None

        if x_relatif < self.largeur_ligne:
            if y_relatif > self.largeur_ligne:
                # Clic sur une ligne verticale
                coup = (ligne, col, 'V')
        else:
            if y_relatif < self.largeur_ligne:
                # Clic sur une ligne horizontale
                coup = (ligne, col, 'H')

        return coup

    def actualiser(self):
        # On supprime les anciennes boîtes et on ajoute les nouvelles.
        self.delete('boite')
        self.dessiner_boites()

        # On supprime les anciennes lignes et on ajoute les nouvelles.
        self.delete('ligne')
        self.dessiner_lignes()

        # On dessine les points
        self.dessiner_points()


class Fenetre(Tk):
    def __init__(self):
        super().__init__()

        # Figer la fenêtre
        self.resizable(0, 0)
        self.config(bg='#eee')

        # Nom de la fenêtre.
        self.title('Pipopipette')

        self.partie = PartiePipopipette()
        # Pour charger d'une partie déjà sauvegardée
        # self.partie = PartiePipopipette('pipopipette/partie_en_cours.txt')

        # Dans le TP, vous voudrez ajouter un attribut self.partie,
        # avec comme valeur une nouvelle Partie
        self.initialiser_canvas()
        self.guess_button = Button(self, width=20, height=3, activebackground='blue', text="Quitter", command=self.quit).grid()
        self.reset_button = Button(self, width=20, height=3, activebackground='blue', bg='yellow', text="Jouer une nouvelle partie", command=self.reset).grid()
        # On lie un clic sur le Canvas à une méthode.
        self.canvas_planche.bind('<Button-1>', self.selectionner)

    def initialiser_canvas(self):
        # Création du canvas grille.
        # Dans le TP, vous voudrez passer self.partie.planche au constructeur
        # de Canvas)
        self.canvas_planche = CanvasPipopipette(self.partie.planche)
        self.canvas_planche.config()
        self.canvas_planche.actualiser()
        self.canvas_planche.grid(pady='20', padx='20')

    def selectionner(self, event):
        '''
        Méthode appelée lorsqu'un clic est fait sur votre fenêtre.

        Par défaut, comme notre fenêtre contient seulement notre Canvas, on va chercher
        le coup associé au clic à l'aide de self.canvas_planche.obtenir_coup_joue(event).

        Ici, pour vous montrer la gestion des exceptions et l'affichage de messages avec
        messagebox, on lance ici une exception ErreurClicPoint et on affiche une erreur si
        le clic a été fait sur un point (associé à un retour None de obtenir_coup_joue()).

        Dans votre TP, le retour de obtenir_coup_joue() sera à None si et seulement si le clic
        N'a PAS été effectué une ligne. Ainsi, si le coup est None, on ne fera rien, sinon on le jouera
        avec self.partie.jouer_coup(). Aussi, si le coup est sur une ligne déjà jouée, on attrapera
        l'exception lancée dans Planche.valider_coup() et on affichera un message d'erreur correspondant.
        Enfin, on s'assurera aussi de faire appel à l'actualisation du canvas et à la logique de
        fin de partie.

        Args:
            event (Event): L'objet Event relié au clic fait sur le canvas
        '''

        coup = self.canvas_planche.obtenir_coup_joue(event)
        # self.partie.planche.jouer_coup(coup, self.partie.joueur_courant.couleur)
        self.partie.jouer_coup(coup)
        # On actualise après chaque clic pour garder un canvas bien arrimé à l'état de la partie.
        self.canvas_planche.actualiser()

        if self.partie.partie_terminee():
            messagebox.showinfo("Window", self.partie.message_fin_partie())

    def reset(self):
        os.execl(sys.executable, sys.executable, *sys.argv)

def main():

    f = Fenetre()
    f.mainloop()