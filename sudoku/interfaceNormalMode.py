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
    validate_input = validation_choice == 'oui'
    
    puzzle, solution = generate_sudoku(size, difficulty)
    fixed_positions = {(r, c) for r in range(size) for c in range(size) if puzzle[r][c] != 0}

    afficher_grille(puzzle, size, fixed_positions)

    while True:
        print(Fore.CYAN + "\nQue souhaitez-vous faire ?")
        print("1. Ajouter un chiffre")
        print("2. Afficher la grille")
        print("3. Annuler le dernier coup (Undo)")
        if not validate_input:
            print("4. Afficher la solution")
        print("5. Quitter")
        print(Fore.RESET)
        
        action = input("Choisissez une option: ")
        
        if action == '1':
            row = int(input("\nEntrez la ligne (0-{}): ".format(size-1)))
            col = int(input("Entrez la colonne (0-{}): ".format(size-1)))
            num = int(input("Entrez le chiffre (1 à {}): ".format(size)))
            
            if (row, col) in fixed_positions:
                print(Fore.RED + "Vous ne pouvez pas modifier un chiffre initial de la grille !" + Fore.RESET)
                continue

            if validate_input:
                if num == solution[row][col]:
                    history.append((row, col, puzzle[row][col]))
                    puzzle[row][col] = num
                else:
                    print(Fore.RED + "Le chiffre est incorrect." + Fore.RESET)
            else:
                history.append((row, col, puzzle[row][col]))
                puzzle[row][col] = num

            afficher_grille(puzzle, size, fixed_positions)
            
            if all(all(cell != 0 for cell in row) for row in puzzle):
                print(Fore.LIGHTGREEN_EX + "\nFélicitations ! Vous avez complété la grille !" + Fore.RESET)
                return

        elif action == '2':
            afficher_grille(puzzle, size, fixed_positions)

        elif action == '3':
            if history:
                row, col, prev_val = history.pop()
                puzzle[row][col] = prev_val
                print(Fore.YELLOW + "Dernier coup annulé." + Fore.RESET)
            else:
                print(Fore.RED + "Aucun coup à annuler." + Fore.RESET)
            afficher_grille(puzzle, size, fixed_positions)
        
        elif action == '4' and not validate_input:
            print(Fore.GREEN + "\nSolution de la grille :" + Fore.RESET)
            afficher_solution(solution, size)
        
        elif action == '5':
            print(Back.WHITE + Fore.LIGHTGREEN_EX + "\nMerci d'avoir joué ! À bientôt !" + Fore.RESET + Back.RESET)
            return
        
        else:
            print(Fore.RED + "Option invalide. Essayez encore." + Fore.RESET)

def afficher_grille(grid, size, fixed_positions):
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
                print(Fore.WHITE + str(num) + Fore.RESET, end="  ")
            else:
                print(Fore.YELLOW + str(num) + Fore.RESET, end="  ")
        print()

def afficher_solution(solution, size):
    box_size = int(size ** 0.5)
    print("\nSolution de la grille :\n")
    for i in range(size):
        if i % box_size == 0 and i != 0:
            print(Fore.GREEN + "-" * (size * 3 + box_size - 1) + Fore.RESET)
        for j in range(size):
            if j % box_size == 0 and j != 0:
                print(Fore.GREEN + "|", end=" " + Fore.RESET)
            print(Fore.WHITE + str(solution[i][j]) + Fore.RESET, end="  ")
        print()
