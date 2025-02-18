import random
from solver import SudokuSolver
from typing import List, Tuple, Optional

class SudokuGenerator:
    def __init__(self, size: int = 9):
        if size not in [4, 9, 16]:  
            raise ValueError("Seules les tailles 4x4, 9x9 et 16x16 sont supportées.")
        
        self.size = size
        self.box_size = int(size ** 0.5)
        self.grid = [[0 for _ in range(size)] for _ in range(size)]

    def is_valid(self, num: int, pos: Tuple[int, int]) -> bool:
        """Vérifie si un nombre peut être placé à une position donnée"""
        row, col = pos
        if num in self.grid[row]:
            return False

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

    def fill_grid(self) -> bool:
        """Remplit entièrement la grille avec une solution valide"""
        empty = self.find_empty()
        if not empty:
            return True 
        row, col = empty

        numbers = list(range(1, self.size + 1))
        random.shuffle(numbers)

        for num in numbers:
            if self.is_valid(num, (row, col)):
                self.grid[row][col] = num

                if self.fill_grid():
                    return True 
                
                self.grid[row][col] = 0 

        return False

    def find_empty(self) -> Optional[Tuple[int, int]]:
        """Trouve une case vide dans la grille"""
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == 0:
                    return (i, j)
        return None

    def remove_numbers(self, difficulty: str = "medium"):
        """Enlève des chiffres de la grille pour créer un puzzle avec une seule solution"""
        difficulties = {
            "easy": int(self.size ** 2 * 0.4),
            "medium": int(self.size ** 2 * 0.5),
            "hard": int(self.size ** 2 * 0.6)
        }
        cells_to_remove = difficulties.get(difficulty, int(self.size ** 2 * 0.5))
        positions = [(i, j) for i in range(self.size) for j in range(self.size)]
        random.shuffle(positions)

        solver = SudokuSolver(self.grid)

        count = 0
        while count < cells_to_remove and positions:
            row, col = positions.pop()
            backup = self.grid[row][col]
            self.grid[row][col] = 0

            grid_copy = [row[:] for row in self.grid]
            solver.grid = grid_copy
            solver.solve_recursive()

            if not self.is_unique_solution():
                self.grid[row][col] = backup 
            else:
                count += 1

    def is_unique_solution(self) -> bool:
        """Vérifie si la grille a une solution unique en utilisant un solveur"""
        solver = SudokuSolver([row[:] for row in self.grid])
        return self.count_solutions(solver) == 1

    def count_solutions(self, solver: SudokuSolver) -> int:
        """Compte le nombre de solutions pour une grille donnée"""
        empty = solver.find_empty()
        if not empty:
            return 1  
        row, col = empty
        count = 0

        for num in range(1, solver.size + 1):
            if solver.is_valid(num, (row, col)):
                solver.grid[row][col] = num
                count += self.count_solutions(solver)
                solver.grid[row][col] = 0

                if count > 1: 
                    return count
        
        return count

    def generate(self, difficulty: str = "medium") -> List[List[int]]:
        """Génère une nouvelle grille de Sudoku avec une difficulté donnée"""
        self.fill_grid() 
        self.remove_numbers(difficulty) 
        return self.grid

if __name__ == "__main__":
    size = None
    while size not in [4, 9, 16]:
        try:
            size = int(input("Choisissez la taille de la grille (4, 9, 16) : ").strip())
            if size not in [4, 9, 16]:
                print("Erreur : Veuillez entrer 4, 9 ou 16.")
        except ValueError:
            print("Erreur : Veuillez entrer un nombre valide.")

    generator = SudokuGenerator(size)
    difficulty = None
    while difficulty not in ["easy", "medium", "hard"]:
        difficulty = input("Choisissez une difficulté (easy, medium, hard) : ").strip().lower()
        if difficulty not in ["easy", "medium", "hard"]:
            print("Erreur : Veuillez entrer 'easy', 'medium' ou 'hard'.")

    grid = generator.generate(difficulty)
    print("\nGrille générée :")
    for row in grid:
        print(" ".join(str(num) if num != 0 else "." for num in row))
