import random
from typing import List, Optional, Tuple
from copy import deepcopy

class SudokuGenerator:
    def __init__(self, size: int = 9):
        self.size = size
        self.box_size = int(size ** 0.5)
        self.grid = [[0 for _ in range(size)] for _ in range(size)]

    def is_valid(self, num: int, pos: Tuple[int, int]) -> bool:
        """Vérifie si un nombre peut être placé à une position donnée"""
        row, col = pos
        
        # Vérifier la ligne
        if num in self.grid[row]:
            return False
            
        # Vérifier la colonne
        for i in range(self.size):
            if self.grid[i][col] == num:
                return False
                
        # Vérifier le carré
        box_x = col // self.box_size
        box_y = row // self.box_size
        for i in range(box_y * self.box_size, box_y * self.box_size + self.box_size):
            for j in range(box_x * self.box_size, box_x * self.box_size + self.box_size):
                if self.grid[i][j] == num:
                    return False
                    
        return True

    def fill_diagonal_boxes(self):
        """Remplit les boîtes diagonales de la grille"""
        for i in range(0, self.size, self.box_size):
            numbers = list(range(1, self.size + 1))
            random.shuffle(numbers)
            pos = 0
            for row in range(i, i + self.box_size):
                for col in range(i, i + self.box_size):
                    self.grid[row][col] = numbers[pos]
                    pos += 1

    def fill_remaining(self, row: int = 0, col: int = 0) -> bool:
        """Remplit le reste de la grille de manière récursive"""
        if col >= self.size:
            row += 1
            col = 0
        if row >= self.size:
            return True

        if self.grid[row][col] != 0:
            return self.fill_remaining(row, col + 1)

        for num in range(1, self.size + 1):
            if self.is_valid(num, (row, col)):
                self.grid[row][col] = num
                if self.fill_remaining(row, col + 1):
                    return True
                self.grid[row][col] = 0

        return False

    def remove_cells(self, difficulty: str) -> None:
        """Retire des cellules selon le niveau de difficulté"""
        difficulties = {
            'easy': self.size * self.size - (self.size * 4),
            'medium': self.size * self.size - (self.size * 3),
            'hard': self.size * self.size - (self.size * 2)
        }
        
        cells_to_remove = difficulties.get(difficulty, self.size * self.size - (self.size * 3))
        cells = [(i, j) for i in range(self.size) for j in range(self.size)]
        random.shuffle(cells)
        
        for i in range(cells_to_remove):
            if i < len(cells):
                row, col = cells[i]
                backup = self.grid[row][col]
                self.grid[row][col] = 0
                
                # Vérifier si la grille a toujours une solution unique
                grid_copy = deepcopy(self.grid)
                if not self.has_unique_solution(grid_copy):
                    self.grid[row][col] = backup

    def has_unique_solution(self, grid: List[List[int]]) -> bool:
        """Vérifie si la grille a une solution unique"""
        def solve(g: List[List[int]], solutions: List[List[List[int]]]) -> None:
            if len(solutions) > 1:
                return
                
            empty = None
            for i in range(self.size):
                for j in range(self.size):
                    if g[i][j] == 0:
                        empty = (i, j)
                        break
                if empty:
                    break
                    
            if not empty:
                solutions.append(deepcopy(g))
                return

            row, col = empty
            for num in range(1, self.size + 1):
                if self.is_valid(num, (row, col)):
                    g[row][col] = num
                    solve(g, solutions)
                    g[row][col] = 0
                    if len(solutions) > 1:
                        return

        solutions = []
        solve(grid, solutions)
        return len(solutions) == 1

    def generate(self, difficulty: str = 'medium') -> List[List[int]]:
        """Génère une nouvelle grille de Sudoku"""
        # Réinitialiser la grille
        self.grid = [[0 for _ in range(self.size)] for _ in range(self.size)]
        
        # Remplir les boîtes diagonales
        self.fill_diagonal_boxes()
        
        # Remplir le reste de la grille
        self.fill_remaining()
        
        # Retirer des cellules selon la difficulté
        self.remove_cells(difficulty)
        
        return self.grid

    def get_difficulty_score(self) -> int:
        """Calcule un score de difficulté pour la grille actuelle"""
        empty_cells = sum(row.count(0) for row in self.grid)
        return empty_cells * 10