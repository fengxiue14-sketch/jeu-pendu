# Jeu du Pendu

Sixième projet de la **Forteresse YUAN**.

## Objectif

Jeu du pendu interactif en Python avec 5 catégories de mots et statistiques persistantes.

## Fonctionnalités

- 5 catégories de mots :
  - Animaux
  - Pays
  - Fruits
  - Metiers
  - Cyber
- Mode "Aléatoire" (catégorie tirée au sort)
- 7 erreurs maximum
- Pendu ASCII art qui évolue
- Affichage des lettres déjà proposées
- Détection des doublons de lettres
- Validation des entrées (une seule lettre A-Z)
- Statistiques persistantes (JSON) :
  - Nombre de parties
  - Victoires / Défaites
  - Taux de victoire
  - Série actuelle et meilleure série

## Installation

Aucune dépendance externe. Python 3.10+ requis.

## Usage

```bash
python pendu.py