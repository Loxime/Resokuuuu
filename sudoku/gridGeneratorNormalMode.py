import random
from copy import deepcopy

def is_valid(grid, row, col, num, size):
    """
    Vérifie si un nombre peut être placé dans la case (row, col).
    Prend en compte les lignes, colonnes et sous-grilles.
    """
    box_size = int(size ** 0.5)

    # Vérifier ligne et colonne
    for i in range(size):
        if grid[row][i] == num or grid[i][col] == num:
            return False
    
    # Vérifier sous-grille
    start_row, start_col = (row // box_size) * box_size, (col // box_size) * box_size
    for i in range(box_size):
        for j in range(box_size):
            if grid[start_row + i][start_col + j] == num:
                return False

    return True

def solve(grid, size):
    """
    Résout la grille de Sudoku avec backtracking.
    """
    for row in range(size):
        for col in range(size):
            if grid[row][col] == 0:
                for num in range(1, size + 1):
                    if is_valid(grid, row, col, num, size):
                        grid[row][col] = num
                        if solve(grid, size):
                            return True
                        grid[row][col] = 0
                return False
    return True

def generate_full_grid(size):
    """
    Génère une grille complète de Sudoku valide.
    """
    grid = [[0 for _ in range(size)] for _ in range(size)]
    
    # Remplissage initial aléatoire pour créer une variation
    for _ in range(size * 2):  # Augmenter si nécessaire pour plus de diversité
        row, col = random.randint(0, size - 1), random.randint(0, size - 1)
        num = random.randint(1, size)
        if is_valid(grid, row, col, num, size):
            grid[row][col] = num

    # Résolution complète pour obtenir une vraie grille de Sudoku
    solve(grid, size)
    
    return grid

def remove_numbers(grid, size, difficulty='medium'):
    """
    Supprime des chiffres de la grille complète pour créer un puzzle avec une difficulté donnée.
    """
    difficulties = {'easy': 0.4, 'medium': 0.5, 'hard': 0.6}  # Pourcentage de cases vides
    num_remove = int(size * size * difficulties.get(difficulty, 0.5))

    puzzle = deepcopy(grid)
    positions = [(i, j) for i in range(size) for j in range(size)]
    random.shuffle(positions)

    for _ in range(num_remove):
        row, col = positions.pop()
        puzzle[row][col] = 0

    return puzzle

def generate_sudoku(size=9, difficulty='medium'):
    """
    Génère une grille de Sudoku avec une taille et une difficulté données.
    """
    full_grid = generate_full_grid(size)
    puzzle = remove_numbers(full_grid, size, difficulty)
    return puzzle, full_grid
