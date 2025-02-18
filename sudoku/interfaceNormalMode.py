from colorama import Fore
from sudoku.gridGeneratorNormalMode import generate_sudoku

def mode_normal():
    """
    Mode normal du jeu, où l'utilisateur choisit la taille et la difficulté de la grille.
    """
    print(Fore.CYAN + "\nMode Normal : Choisissez la taille et la difficulté de la grille" + Fore.RESET)

    size_options = {1: 3, 2: 6, 3: 9}
    print("1. Grille 3x3")
    print("2. Grille 6x6")
    print("3. Grille 9x9")
    
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
    # Affichage initial de la grille
    afficher_grille(puzzle, size, validate_input)

    # Boucle principale du jeu
    action = ''
    while action != '3':  # On continue jusqu'à ce que l'utilisateur choisisse de quitter
        action = input(Fore.CYAN + "\nQue souhaitez-vous faire ?\n1. Ajouter un chiffre\n2. Afficher la grille\n3. Quitter\nChoisissez une option (1/2/3): ")
        
        if action == '1':
            # Demander à l'utilisateur où ajouter un chiffre
            row = int(input("\nEntrez la colonne (en partant de la droite) où vous souhaitez ajouter un chiffre : "))
            col = int(input("Entrez la ligne (en partant du haut) où vous souhaitez ajouter un chiffre : "))
            num = int(input("Entrez le chiffre (1 à " + str(size) + "): "))
            
            if row < 0 or row >= size or col < 0 or col >= size:
                print(Fore.RED + "Coordonnées invalides. Essayez encore." + Fore.RESET)
                continue
            
            if validate_input:
                if is_valid(puzzle, row, col, num, size):
                    puzzle[row][col] = num
                else:
                    print(Fore.RED + "Le chiffre ne peut pas être placé ici." + Fore.RESET)
            else:
                puzzle[row][col] = num

            afficher_grille(puzzle, size, validate_input)

        elif action == '2':
            afficher_grille(puzzle, size, validate_input)

        elif action == '3':
            print(Fore.GREEN + "Merci d'avoir joué ! À bientôt !" + Fore.RESET)

        else:
            print(Fore.RED + "Option invalide. Essayez encore." + Fore.RESET)

def afficher_grille(grid, size, validate_input):
    """
    Affiche la grille de Sudoku et gère les entrées de l'utilisateur.
    """
    print("\nGrille actuelle :")
    for row in grid:
        print(" ".join(str(num) if num != 0 else '.' for num in row))

def is_valid(grid, row, col, num, size):
    """
    Vérifie si un nombre peut être placé dans la case (row, col).
    La vérification prend en compte la taille de la grille (3x3, 6x6, 9x9).
    """
    for i in range(size):
        if grid[row][i] == num or grid[i][col] == num:
            return False
    
    box_size = int(size ** 0.5)
    start_row, start_col = box_size * (row // box_size), box_size * (col // box_size)
    for i in range(box_size):
        for j in range(box_size):
            if grid[start_row + i][start_col + j] == num:
                return False
    
    return True
