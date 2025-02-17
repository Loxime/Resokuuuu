import colorama
from colorama import Fore
from interface import mode_normal, mode_sandbox  # Importation des modes de jeu

colorama.init()

def afficher_menu_principal():
    """
    Affiche le menu principal du jeu.
    """
    print(Fore.CYAN + "\nBienvenue dans le Sudoku!\n" + Fore.RESET)
    print("1. Mode Normal (Jeu avec grille générée)")
    print("2. Mode Sandbox (Créez votre propre grille)")
    print("3. Quitter")
    
def choisir_mode():
    """
    Permet à l'utilisateur de choisir un mode.
    """
    continue_program = True 
    
    while continue_program:
        afficher_menu_principal()
        choix = input("Veuillez choisir une option (1/2/3): ")
        
        if choix == '1':
            mode_normal()  # Redirige vers le mode normal du jeu
        elif choix == '2':
            mode_sandbox()  # Redirige vers le mode sandbox pour créer une grille personnalisée
        elif choix == '3':
            print("Merci d'avoir joué! À bientôt!")
            continue_program = False  # Change la variable de contrôle pour arrêter la boucle
        else:
            print(Fore.RED + "Choix invalide, essayez encore." + Fore.RESET)

if __name__ == "__main__":
    choisir_mode()  # Lancement du menu principal
