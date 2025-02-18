import random
from solver import SudokuSolver
from typing import List, Tuple

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

        # Vérifier la boîte 3x3
        box_x = col // self.box_size
        box_y = row // self.box_size
        for i in range(box_y * self.box_size, box_y * self.box_size + self.box_size):
            for j in range(box_x * self.box_size, box_x * self.box_size + self.box_size):
                if self.grid[i][j] == num:
                    return False

        return True

    def fill_grid(self) -> bool:
        """Remplit entièrement la grille avec une solution valide"""
        empty = self.find_empty()
        if not empty:
            return True  # La grille est complète

        row, col = empty
        numbers = list(range(1, self.size + 1))
        random.shuffle(numbers)

        for num in numbers:
            if self.is_valid(num, (row, col)):
                self.grid[row][col] = num
                if self.fill_grid():
                    return True
                self.grid[row][col] = 0  # Backtracking

        return False

    def find_empty(self) -> Tuple[int, int] or None:
        """Trouve une case vide dans la grille"""
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == 0:
                    return i, j
        return None

    def remove_numbers(self, difficulty: str = "medium"):
        """Enlève des chiffres de la grille pour créer un puzzle avec une seule solution"""
        difficulties = {
            "easy": 35,
            "medium": 45,
            "hard": 55
        }
        cells_to_remove = difficulties.get(difficulty, 45)

        # Créer une liste des positions à vider
        positions = [(i, j) for i in range(self.size) for j in range(self.size)]
        random.shuffle(positions)

        solver = SudokuSolver(self.grid)

        for _ in range(cells_to_remove):
            row, col = positions.pop()
            backup = self.grid[row][col]
            self.grid[row][col] = 0

            # Vérifier si la grille a toujours une solution unique
            grid_copy = [row[:] for row in self.grid]
            solver.grid = grid_copy
            solver.solve_recursive()

            # Si plusieurs solutions existent, restaurer la case
            if not self.is_unique_solution():
                self.grid[row][col] = backup

    def is_unique_solution(self) -> bool:
        """Vérifie si la grille a une solution unique en utilisant un solveur"""
        solver = SudokuSolver([row[:] for row in self.grid])
        solutions_count = self.count_solutions(solver)
        return solutions_count == 1

    def count_solutions(self, solver: SudokuSolver) -> int:
        """Compte le nombre de solutions pour une grille donnée"""
        empty = solver.find_empty()
        if not empty:
            return 1  # Une solution trouvée

        row, col = empty
        count = 0

        for num in range(1, solver.size + 1):
            if solver.is_valid(num, (row, col)):
                solver.grid[row][col] = num
                count += self.count_solutions(solver)
                if count > 1:  # Si plus d'une solution, on arrête
                    break
                solver.grid[row][col] = 0

        return count

    def generate(self, difficulty: str = "medium") -> List[List[int]]:
        """Génère une nouvelle grille de Sudoku avec une difficulté donnée"""
        self.fill_grid()
        self.remove_numbers(difficulty)
        return self.grid

if __name__ == "__main__":
    generator = SudokuGenerator()
    difficulty = input("Choisissez une difficulté (easy, medium, hard) : ").strip().lower()
    grid = generator.generate(difficulty)

    print("\nGrille générée :")
    for row in grid:
        print(" ".join(str(num) if num != 0 else "." for num in row))