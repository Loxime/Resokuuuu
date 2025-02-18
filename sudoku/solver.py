from typing import List, Tuple, Optional, Set
from collections import deque
import time

class SudokuSolver:
    def __init__(self, grid: List[List[int]]):
        self.grid = grid
        self.size = len(grid)
        self.box_size = int(self.size ** 0.5)

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
        box_x = pos[1] // self.box_size
        box_y = pos[0] // self.box_size
        for i in range(box_y * self.box_size, box_y * self.box_size + self.box_size):
            for j in range(box_x * self.box_size, box_x * self.box_size + self.box_size):
                if self.grid[i][j] == num:
                    return False
                    
        return True

    def find_empty(self) -> Optional[Tuple[int, int]]:
        """Trouve une case vide dans la grille"""
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == 0:
                    return (i, j)
        return None

    def solve_recursive(self) -> bool:
        """Résout le Sudoku avec backtracking récursif"""
        empty = self.find_empty()
        if not empty:
            return True

        row, col = empty
        for num in range(1, self.size + 1):
            if self.is_valid(num, (row, col)):
                self.grid[row][col] = num
                if self.solve_recursive():
                    return True
                self.grid[row][col] = 0
                
        return False

    def get_possible_values(self, pos: Tuple[int, int]) -> Set[int]:
        """Retourne l'ensemble des valeurs possibles pour une position donnée"""
        values = set()
        for num in range(1, self.size + 1):
            if self.is_valid(num, pos):
                values.add(num)
        return values


    def solve_mrv(self) -> bool:
        """Résout le Sudoku en utilisant l'heuristique Minimum Remaining Values"""
        empty = self.find_empty()
        if not empty:
            return True

        # Trouver la cellule avec le moins de valeurs possibles
        min_values = self.size + 1
        best_cell = None
        best_values = set()
        
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == 0:
                    values = self.get_possible_values((i, j))
                    if len(values) < min_values:
                        min_values = len(values)
                        best_cell = (i, j)
                        best_values = values
                        if min_values == 1:  # Optimisation : case avec une seule possibilité
                            break

        if best_cell is None:
            return True

        row, col = best_cell
        for num in best_values:
            self.grid[row][col] = num
            if self.solve_mrv():
                return True
            self.grid[row][col] = 0

        return False

    def solve_iterative(self) -> bool:
        """Résout le Sudoku de manière itérative avec une pile"""
        stack = deque()
        empty = self.find_empty()
        if not empty:
            return True

        # État initial
        stack.append((empty, 1))  # (position, valeur_courante)
        
        while stack:
            pos, num = stack[-1]
            row, col = pos
            
            # Essayer les valeurs de num à 9
            found = False
            while num <= self.size and not found:
                if self.is_valid(num, pos):
                    self.grid[row][col] = num
                    next_empty = self.find_empty()
                    if not next_empty:
                        return True
                    stack.append((next_empty, 1))
                    found = True
                num += 1
            
            if not found:
                self.grid[row][col] = 0
                stack.pop()
                if stack:
                    last_pos, last_num = stack[-1]
                    stack[-1] = (last_pos, last_num + 1)

        return False


    def benchmark_solvers(self) -> dict:
        """Compare les performances des différents solveurs"""
        results = {}
        grid_copy = [row[:] for row in self.grid]  # Garde une copie de la grille initiale

        # Test du solveur récursif
        self.grid = [row[:] for row in grid_copy]
        start = time.time()
        recursive_solved = self.solve_recursive()
        results['recursive'] = {
            'time': time.time() - start,
            'solved': recursive_solved
        }

        # Test du solveur MRV
        self.grid = [row[:] for row in grid_copy]
        start = time.time()
        mrv_solved = self.solve_mrv()
        results['mrv'] = {
            'time': time.time() - start,
            'solved': mrv_solved
        }

        # Test du solveur itératif
        self.grid = [row[:] for row in grid_copy]
        start = time.time()
        iterative_solved = self.solve_iterative()
        results['iterative'] = {
            'time': time.time() - start,
            'solved': iterative_solved
        }

        return results