#!/usr/bin/env python3
"""
Jeu du Pendu - Projet 06 de la Forteresse YUAN.
Deviner un mot secret en 7 erreurs max.
"""

import random
import sys
from pathlib import Path
from datetime import datetime
import json


STATS_FILE = Path(__file__).parent / "stats.json"
MAX_ERREURS = 7


MOTS = {
    "Animaux": ["CHAT", "CHIEN", "LION", "TIGRE", "ELEPHANT", "GIRAFE", "SERPENT", "AIGLE", "DAUPHIN", "REQUIN"],
    "Pays": ["FRANCE", "BURKINA", "JAPON", "CANADA", "BRESIL", "EGYPTE", "CHINE", "INDE", "RUSSIE", "MAROC"],
    "Fruits": ["POMME", "BANANE", "ORANGE", "FRAISE", "CERISE", "MANGUE", "ANANAS", "KIWI", "RAISIN", "PECHE"],
    "Metiers": ["MEDECIN", "INGENIEUR", "AVOCAT", "PROFESSEUR", "POMPIER", "PILOTE", "CUISINIER", "ARCHITECTE", "DENTISTE", "JOURNALISTE"],
    "Cyber": ["HACKER", "FIREWALL", "MALWARE", "RESEAU", "ENCRYPTION", "PASSWORD", "SECURITE", "VULNERABILITE", "PENTEST", "RANSOMWARE"],
}


PENDU_ART = [
    # 0 erreurs
    """
     +---+
     |   |
         |
         |
         |
         |
    =========
    """,
    # 1 erreur
    """
     +---+
     |   |
     O   |
         |
         |
         |
    =========
    """,
    # 2 erreurs
    """
     +---+
     |   |
     O   |
     |   |
         |
         |
    =========
    """,
    # 3 erreurs
    """
     +---+
     |   |
     O   |
    /|   |
         |
         |
    =========
    """,
    # 4 erreurs
    """
     +---+
     |   |
     O   |
    /|\\  |
         |
         |
    =========
    """,
    # 5 erreurs
    """
     +---+
     |   |
     O   |
    /|\\  |
    /    |
         |
    =========
    """,
    # 6 erreurs
    """
     +---+
     |   |
     O   |
    /|\\  |
    / \\  |
         |
    =========
    """,
    # 7 erreurs (perdu)
    """
     +---+
     |   |
     O   |
    /|\\  |
    / \\  |
         |
    =========
    """,
]


# ============================================================
# STATISTIQUES
# ============================================================

def charger_stats():
    """Charge les statistiques."""
    if not STATS_FILE.exists():
        return {"parties": 0, "victoires": 0, "defaites": 0, "serie": 0, "meilleure_serie": 0}
    try:
        with open(STATS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {"parties": 0, "victoires": 0, "defaites": 0, "serie": 0, "meilleure_serie": 0}


def sauvegarder_stats(stats):
    """Sauvegarde les statistiques."""
    try:
        with open(STATS_FILE, "w", encoding="utf-8") as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
    except IOError as e:
        print(f"[AVERTISSEMENT] {e}", file=sys.stderr)


# ============================================================
# AFFICHAGE
# ============================================================

def afficher_titre(titre):
    """Affiche un titre encadre."""
    print()
    print("=" * 60)
    print(f"  {titre}")
    print("=" * 60)


def afficher_etat(mot, lettres_trouvees, lettres_proposees, erreurs):
    """Affiche l'état du jeu."""
    # Mot avec tirets
    affichage = " ".join(c if c in lettres_trouvees else "_" for c in mot)
    
    print(f"\n  Mot : {affichage}")
    print(f"  Lettres proposees : {', '.join(sorted(lettres_proposees)) if lettres_proposees else '(aucune)'}")
    print(f"  Erreurs : {erreurs}/{MAX_ERREURS}")
    print(PENDU_ART[erreurs])


# ============================================================
# CHOIX DU MOT
# ============================================================

def choisir_categorie():
    """Menu de choix de catégorie."""
    afficher_titre("Choisis une catégorie")
    
    categories = list(MOTS.keys())
    for i, cat in enumerate(categories, 1):
        print(f"  {i}. {cat}")
    print(f"  {len(categories) + 1}. Aléatoire")
    print("  0. Retour")
    
    while True:
        try:
            choix = input("Ton choix : ").strip()
            if choix == "0":
                return None
            idx = int(choix) - 1
            if 0 <= idx < len(categories):
                return categories[idx]
            if idx == len(categories):
                return random.choice(categories)
            print("Choix invalide.")
        except ValueError:
            print("Entre un nombre.")


# ============================================================
# BOUCLE DE JEU
# ============================================================

def jouer_partie(categorie):
    """Joue une partie complète."""
    mot = random.choice(MOTS[categorie])
    lettres_trouvees = set()
    lettres_proposees = set()
    erreurs = 0
    
    afficher_titre(f"Partie - {categorie}")
    print(f"Mot de {len(mot)} lettres. Tu as {MAX_ERREURS} erreurs max.")
    print("Tape 'quit' pour abandonner.\n")
    
    while erreurs < MAX_ERREURS:
        afficher_etat(mot, lettres_trouvees, lettres_proposees, erreurs)
        
        # Victoire ?
        if all(c in lettres_trouvees for c in mot):
            print(f"\n[BINGO] Bravo ! Le mot était : {mot}")
            return "victoire"
        
        # Demander une lettre
        try:
            ligne = input("  Ta lettre : ").strip().upper()
        except (EOFError, KeyboardInterrupt):
            print("\n\nInterrompu.")
            return "abandon"
        
        if ligne in ("QUIT", "Q", "ABANDON"):
            print(f"\nTu abandonnes. Le mot était : {mot}")
            return "abandon"
        
        if len(ligne) != 1 or not ligne.isalpha():
            print("  ⚠️  Tape une seule lettre (A-Z).")
            continue
        
        if ligne in lettres_proposees:
            print(f"  ⚠️  Tu as déjà proposé {ligne}.")
            continue
        
        lettres_proposees.add(ligne)
        
        if ligne in mot:
            lettres_trouvees.add(ligne)
            print(f"  ✅ Bien joué ! '{ligne}' est dans le mot.")
        else:
            erreurs += 1
            print(f"  ❌ Raté ! '{ligne}' n'est pas dans le mot.")
    
    # Perdu
    afficher_etat(mot, lettres_trouvees, lettres_proposees, erreurs)
    print(f"\n[PERDU] Le mot était : {mot}")
    return "defaite"


# ============================================================
# MENU PRINCIPAL
# ============================================================

def afficher_stats(stats):
    """Affiche les statistiques."""
    afficher_titre("Statistiques")
    print(f"  Parties jouées    : {stats['parties']}")
    print(f"  Victoires         : {stats['victoires']}")
    print(f"  Défaites          : {stats['defaites']}")
    if stats['parties'] > 0:
        taux = round(stats['victoires'] / stats['parties'] * 100, 1)
        print(f"  Taux de victoire  : {taux}%")
    print(f"  Série actuelle    : {stats['serie']}")
    print(f"  Meilleure série   : {stats['meilleure_serie']}")


def menu_principal():
    """Menu principal."""
    stats = charger_stats()
    
    while True:
        afficher_titre("JEU DU PENDU")
        print(f"  {stats['parties']} partie(s) — Série actuelle : {stats['serie']}")
        print()
        print("  1. Nouvelle partie")
        print("  2. Voir les statistiques")
        print("  3. Quitter")
        print("=" * 60)
        
        choix = input("Ton choix : ").strip()
        
        if choix == "1":
            categorie = choisir_categorie()
            if categorie is None:
                continue
            
            resultat = jouer_partie(categorie)
            
            if resultat != "abandon":
                stats["parties"] += 1
                if resultat == "victoire":
                    stats["victoires"] += 1
                    stats["serie"] += 1
                    if stats["serie"] > stats["meilleure_serie"]:
                        stats["meilleure_serie"] = stats["serie"]
                else:
                    stats["defaites"] += 1
                    stats["serie"] = 0
                sauvegarder_stats(stats)
        
        elif choix == "2":
            afficher_stats(stats)
        
        elif choix == "3":
            print("\nAu revoir !")
            break
        
        else:
            print("Choix invalide.")


def main():
    """Point d'entrée."""
    print()
    print("=" * 60)
    print("  JEU DU PENDU v1.0")
    print("  Projet 06 - Forteresse YUAN")
    print("=" * 60)
    
    try:
        menu_principal()
    except KeyboardInterrupt:
        print("\n\nInterrompu. Au revoir !")
        return 1
    except Exception as e:
        print(f"\n[FATAL] {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())