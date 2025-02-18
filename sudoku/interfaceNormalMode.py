from colorama import Fore, Back
from gridGeneratorNormalMode import generate_sudoku

# Historique des coups pour le undo
history = []

def mode_normal():
    """
    Mode normal du jeu, où l'utilisateur choisit la taille et la difficulté de la grille.
    """
    print(Fore.CYAN + "\nMode Normal : Choisissez la taille et la difficulté de la grille\n" + Fore.RESET)

    size_options = {1: 4, 2: 9, 3: 16} 
    print("1. Grille 4x4")
    print("2. Grille 9x9")
    print("3. Grille 16x16")
    
    size_choice = input("Choisissez la taille de la grille (1/2/3): ")
    size = size_options.get(int(size_choice), 9)  # Par défaut, on prend la grille 9x9 si invalide

    difficulty_options = {'1': 'easy', '2': 'medium', '3': 'hard'}
    print("\nChoisissez la difficulté :")
    print("1. Facile")
    print("2. Moyen")
    print("3. Difficile")

    difficulty_choice = input("Choisissez la difficulté (1/2/3): ")
    difficulty = difficulty_options.get(difficulty_choice, 'medium')

    validation_choice = input("Souhaitez-vous activer la validation des entrées ? (oui/non): ").lower()
    validate_input = True if validation_choice == 'oui' else False
    
    puzzle, solution = generate_sudoku(size, difficulty)
    fixed_positions = {(r, c) for r in range(size) for c in range(size) if puzzle[r][c] != 0}  # Sauvegarde des chiffres initiaux

    # Affichage initial de la grille
    afficher_grille(puzzle, size, fixed_positions)

    # Boucle principale du jeu
    action = ''
    while action != '4':  # On continue jusqu'à ce que l'utilisateur choisisse de quitter
        action = input(Fore.CYAN + "\nQue souhaitez-vous faire ?\n1. Ajouter un chiffre\n2. Afficher la grille\n3. Annuler le dernier coup (Undo)\n4. Quitter\nChoisissez une option (1/2/3/4): " + Fore.RESET)
        
        if action == '1':
            # Demander à l'utilisateur où ajouter un chiffre
            row = int(input("\nEntrez la ligne (0-{}): ".format(size-1)))
            col = int(input("Entrez la colonne (0-{}): ".format(size-1)))
            num = int(input("Entrez le chiffre (1 à " + str(size) + "): "))
            
            if row < 0 or row >= size or col < 0 or col >= size:
                print(Fore.RED + "Coordonnées invalides. Essayez encore." + Fore.RESET)
                continue
            
            if (row, col) in fixed_positions:
                print(Fore.RED + "Vous ne pouvez pas modifier un chiffre initial de la grille !" + Fore.RESET)
                continue

            if validate_input:
                if num == solution[row][col]:  # Comparaison avec la solution sauvegardée
                    history.append((row, col, puzzle[row][col]))  # Sauvegarde pour undo
                    puzzle[row][col] = num
                else:
                    print(Fore.RED + "Le chiffre est incorrect." + Fore.RESET)
            else:
                history.append((row, col, puzzle[row][col]))
                puzzle[row][col] = num

            afficher_grille(puzzle, size, fixed_positions)
        
        elif action == '2':
            afficher_grille(puzzle, size, fixed_positions)

        elif action == '3':  # Undo
            if history:
                row, col, prev_val = history.pop()
                puzzle[row][col] = prev_val
                print(Fore.YELLOW + "Dernier coup annulé." + Fore.RESET)
            else:
                print(Fore.RED + "Aucun coup à annuler." + Fore.RESET)
            afficher_grille(puzzle, size, fixed_positions)

        elif action == '4':
            print(Back.WHITE + Fore.LIGHTGREEN_EX + "\nMerci d'avoir joué ! À bientôt !" + Fore.RESET + Back.RESET)

        else:
            print(Fore.RED + "Option invalide. Essayez encore." + Fore.RESET)

def afficher_grille(grid, size, fixed_positions):
    """
    Affiche la grille de Sudoku avec des bordures visuelles et mise en couleur.
    """
    box_size = int(size ** 0.5)
    print("\nGrille actuelle :\n")
    for i in range(size):
        if i % box_size == 0 and i != 0:
            print(Fore.BLUE + "-" * (size * 3 + box_size - 1) + Fore.RESET)
        for j in range(size):
            if j % box_size == 0 and j != 0:
                print(Fore.BLUE + "|", end=" " + Fore.RESET)
            num = grid[i][j]
            if num == 0:
                print(". ", end=" ")
            elif (i, j) in fixed_positions:
                print(Fore.WHITE + str(num) + Fore.RESET, end="  ")  # Blanc pour chiffres initiaux
            else:
                print(Fore.YELLOW + str(num) + Fore.RESET, end="  ")  # Jaune pour entrées utilisateur
        print()
