import random

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

def count_empty_cells(grid):
    """
    Compte le nombre de cases vides dans la grille.
    """
    return sum(row.count(0) for row in grid)

def count_possible_values(grid, size):
    """
    Compte le nombre total de possibilités pour toutes les cases vides.
    Plus le nombre de choix est élevé, plus la grille est facile.
    """
    total_possibilities = 0
    for row in range(size):
        for col in range(size):
            if grid[row][col] == 0:
                possibilities = sum(1 for num in range(1, size + 1) if is_valid(grid, row, col, num, size))
                total_possibilities += possibilities
    
    return total_possibilities

def count_initial_constraints(grid):
    """
    Compte le nombre de contraintes initiales générées par les chiffres déjà placés.
    Plus ce nombre est élevé, plus la grille est facile.
    """
    constraints = 0
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] != 0:
                constraints += 1
    return constraints

def evaluate_difficulty(grid, size):
    """
    Évalue la difficulté d'une grille de Sudoku en combinant le nombre de cases vides,
    les possibilités et les contraintes initiales.
    """
    empty_cells = count_empty_cells(grid)
    possible_values = count_possible_values(grid, size)
    initial_constraints = count_initial_constraints(grid)
    
    if empty_cells < size * 0.4 or possible_values > size * 15 or initial_constraints > size * 0.3:
        return "Facile"
    elif empty_cells < size * 0.5 or possible_values > size * 10 or initial_constraints > size * 0.2:
        return "Moyen"
    else:
        return "Difficile"
