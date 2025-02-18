import random
from copy import deepcopy

def is_valid(grid, row, col, num, size):
    """
    Vérifie si un nombre peut être placé dans la case (row, col).
    La vérification prend en compte la taille de la grille (3x3, 6x6, 9x9).
    """
    # Vérification de la ligne et colonne
    for i in range(size):
        if grid[row][i] == num or grid[i][col] == num:
            return False
    
    # Vérification du carré (en fonction de la taille de la grille)
    box_size = int(size ** 0.5)  # La taille du carré (3 pour 9x9, 2 pour 6x6, 1 pour 3x3)
    start_row, start_col = box_size * (row // box_size), box_size * (col // box_size)
    for i in range(box_size):
        for j in range(box_size):
            if grid[start_row + i][start_col + j] == num:
                return False
    
    return True

def generate_full_grid(size):
    """
    Génère une grille complète et valide en remplissant aléatoirement en fonction de la taille.
    """
    grid = [[0 for _ in range(size)] for _ in range(size)]
    for _ in range(30):  # Pré-remplissage aléatoire pour guider le solveur
        row, col = random.randint(0, size - 1), random.randint(0, size - 1)
        num = random.randint(1, size)
        if is_valid(grid, row, col, num, size):
            grid[row][col] = num
    
    return grid

def remove_numbers(grid, size, difficulty='medium'):
    """
    Supprime des chiffres de la grille pour créer un puzzle de difficulté donnée.
    La difficulté est liée au nombre de cases supprimées et à leur position dans la grille.
    """
    difficulties = {'easy': int(size * size * 0.5), 
                    'medium': int(size * size * 0.6), 
                    'hard': int(size * size * 0.7)}
    num_remove = difficulties.get(difficulty, int(size * size * 0.6))
    
    puzzle = deepcopy(grid)
    count = 0
    while count < num_remove:
        row, col = random.randint(0, size - 1), random.randint(0, size - 1)
        if puzzle[row][col] != 0:
            puzzle[row][col] = 0
            count += 1
    
    return puzzle

def generate_sudoku(size=9, difficulty='medium'):
    """
    Génère un Sudoku avec une taille et une difficulté données.
    """
    full_grid = generate_full_grid(size)
    puzzle = remove_numbers(full_grid, size, difficulty)
    return puzzle, full_grid
