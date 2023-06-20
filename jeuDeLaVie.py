# -*- coding: utf-8 -*-

"""
Jeu de la Vie interactif

Clic gauche pour ajouter des cellules

Clic droit pour commencer/arrêter la simulation

Clic molette pour appuyer sur un bouton
"""

import pygame
import numpy as np
import time

largeur, hauteur = 800, 800
cellule_taille = 10

pygame.init()
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Jeu de la vie")

couleur_fond = (255, 255, 255)
couleur_cellule_morte = (255, 255, 255)
couleur_cellule_vivante = (0, 0, 0)
couleur_texte = (0, 0, 0)
couleur_bouton = (200, 200, 200)
couleur_bouton_survol = (150, 150, 150)

police = pygame.font.SysFont(None, 24)
grille_largeur, grille_hauteur = largeur // cellule_taille, hauteur // cellule_taille
grille = np.zeros((grille_largeur, grille_hauteur), dtype=bool)

temps_ecoule = 0
temps_interval = 500
generations = 0
grille_aleatoire = False

def generer_grille_aleatoire():
    global grille
    grille = np.random.choice([False, True], size=(grille_largeur, grille_hauteur))

en_cours = True
pause = True
while en_cours:
    fenetre.fill(couleur_fond)

    # Gestion des événements
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            en_cours = False
        elif evenement.type == pygame.MOUSEBUTTONDOWN:
            if evenement.button == 1:  # Clic gauche
                x, y = evenement.pos
                if not grille_aleatoire_rect.collidepoint((x, y)) and y < grille_hauteur * cellule_taille:
                    i, j = x // cellule_taille, y // cellule_taille
                    grille[i, j] = not grille[i, j]
            elif evenement.button == 3:  # Clic droit
                pause = not pause
            elif evenement.button == 2 and grille_aleatoire_rect.collidepoint(evenement.pos):  # Clic molette sur le bouton de génération aléatoire
                generer_grille_aleatoire()
                generations = 0
                temps_ecoule = pygame.time.get_ticks()

    # Mise à jour de la grille si le jeu n'est pas en pause et le temps écoulé est supérieur à l'intervalle spécifié
    if not pause and pygame.time.get_ticks() - temps_ecoule > temps_interval:
        # Copie temporaire de la grille pour la mise à jour
        nouvelle_grille = grille.copy()

        # Mise à jour de la grille
        for i in range(grille_largeur):
            for j in range(grille_hauteur):
                # Comptage des voisins vivants
                voisins_vivants = np.sum(grille[max(i - 1, 0):min(i + 2, grille_largeur), max(j - 1, 0):min(j + 2, grille_hauteur)]) - grille[i, j]

                # Règles du jeu
                if grille[i, j]:
                    if voisins_vivants < 2 or voisins_vivants > 3:
                        nouvelle_grille[i, j] = False
                else:
                    if voisins_vivants == 3:
                        nouvelle_grille[i, j] = True

        grille = nouvelle_grille
        generations += 1
        temps_ecoule = pygame.time.get_ticks()

    # Affichage
    for i in range(grille_largeur):
        for j in range(grille_hauteur):
            x, y = i * cellule_taille, j * cellule_taille
            if grille[i, j]:
                pygame.draw.rect(fenetre, couleur_cellule_vivante, (x, y, cellule_taille, cellule_taille))
            else:
                pygame.draw.rect(fenetre, couleur_cellule_morte, (x, y, cellule_taille, cellule_taille))

    # Affichage du compteur de générations
    texte = police.render("Générations : {}".format(generations), True, couleur_texte)
    fenetre.blit(texte, (largeur - texte.get_width() - 10, hauteur - texte.get_height() - 10))

    # Affichage du bouton aléatoire
    texte_bouton = police.render("Générer aléatoirement", True, couleur_texte)
    bouton_largeur, bouton_hauteur = texte_bouton.get_width() + 10, texte_bouton.get_height() + 10
    bouton_x, bouton_y = 10, hauteur - bouton_hauteur - 10
    grille_aleatoire_rect = pygame.Rect(bouton_x, bouton_y, bouton_largeur, bouton_hauteur)
    pygame.draw.rect(fenetre, couleur_bouton, grille_aleatoire_rect)
    fenetre.blit(texte_bouton, (bouton_x + 5, bouton_y + 5))

    # Couleur du bouton lorsqu'il est survolé
    if grille_aleatoire_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(fenetre, couleur_bouton_survol, grille_aleatoire_rect)

    # Mise à jour de l'affichage
    pygame.display.flip()

pygame.quit()

