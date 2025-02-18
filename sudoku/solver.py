from typing import List, Tuple, Optional, Set
from collections import deque
import time
import os

class SudokuSolver:
    def __init__(self, grid: List[List[int]], step_by_step: bool = False):
        self.grid = grid
        self.size = len(grid)
        self.box_size = int(self.size ** 0.5)
        self.step_by_step = step_by_step  # Mode pas à pas

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

        # Vérifier la sous-grille
        box_x = col // self.box_size
        box_y = row // self.box_size
        for i in range(box_y * self.box_size, (box_y + 1) * self.box_size):
            for j in range(box_x * self.box_size, (box_x + 1) * self.box_size):
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

    def print_grid(self):
        """Affiche la grille de Sudoku"""
        os.system('cls' if os.name == 'nt' else 'clear')  # Effacer la console pour une meilleure visibilité
        for i in range(self.size):
            if i % self.box_size == 0 and i != 0:
                print("-" * (self.size * 2 + self.box_size))
            for j in range(self.size):
                if j % self.box_size == 0 and j != 0:
                    print(" | ", end="")
                print(self.grid[i][j] if self.grid[i][j] != 0 else ".", end=" ")
            print()
        time.sleep(0.3)  # Pause pour que l'utilisateur voie l'évolution

    def solve_recursive(self) -> bool:
        """Résout le Sudoku avec backtracking récursif"""
        empty = self.find_empty()
        if not empty:
            return True  # La grille est résolue
        row, col = empty

        for num in range(1, self.size + 1):
            if self.is_valid(num, (row, col)):
                self.grid[row][col] = num
                if self.step_by_step:
                    self.print_grid()  # Afficher l'état actuel de la grille

                if self.solve_recursive():
                    return True
                
                self.grid[row][col] = 0  # Annulation

        return False

    def solve_mrv(self) -> bool:
        """Résout le Sudoku en utilisant l'heuristique Minimum Remaining Values"""
        empty = self.find_empty()
        if not empty:
            return True
        min_values = self.size + 1
        best_cell = None
        best_values = set()

        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == 0:
                    values = {num for num in range(1, self.size + 1) if self.is_valid(num, (i, j))}
                    if len(values) < min_values:
                        min_values = len(values)
                        best_cell = (i, j)
                        best_values = values
        
        if best_cell is None:
            return True
        
        row, col = best_cell
        for num in best_values:
            self.grid[row][col] = num
            if self.step_by_step:
                self.print_grid()

            if self.solve_mrv():
                return True

            self.grid[row][col] = 0  # Annulation

        return False

    def solve_iterative(self) -> bool:
        """Résout le Sudoku de manière itérative avec une pile"""
        stack = deque()
        empty = self.find_empty()
        if not empty:
            return True
        stack.append((empty, 1))

        while stack:
            pos, num = stack[-1]
            row, col = pos

            found = False
            while num <= self.size and not found:
                if self.is_valid(num, pos):
                    self.grid[row][col] = num
                    if self.step_by_step:
                        self.print_grid()

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

    def solve_forward_checking(self) -> bool:
        """Résout le Sudoku en utilisant l'heuristique Forward Checking"""
        empty = self.find_empty()
        if not empty:
            return True
        row, col = empty

        for num in range(1, self.size + 1):
            if self.is_valid(num, (row, col)):
                self.grid[row][col] = num
                if self.forward_check():
                    if self.step_by_step:
                        self.print_grid()
                    if self.solve_forward_checking():
                        return True
                self.grid[row][col] = 0

        return False

    def forward_check(self) -> bool:
        """Applique l'heuristique Forward Checking pour réduire les domaines des variables"""
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == 0:
                    if not {num for num in range(1, self.size + 1) if self.is_valid(num, (i, j))}:
                        return False
        return True

    def benchmark_solvers(self) -> dict:
        """Compare les performances des différents solveurs"""
        results = {}
        original_grid = [row[:] for row in self.grid]

        solvers = {
            "recursive": self.solve_recursive,
            "mrv": self.solve_mrv,
            "iterative": self.solve_iterative,
            "forward_checking": self.solve_forward_checking
        }

        for name, solver in solvers.items():
            self.grid = [row[:] for row in original_grid]
            start = time.perf_counter()
            solved = solver()
            end = time.perf_counter()

            results[name] = {
                "time": end - start,
                "solved": solved
            }

        self.grid = [row[:] for row in original_grid]
        return results
