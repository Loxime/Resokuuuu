import sys
from typing import List, Optional, Tuple
import random
import time
import colorama
from colorama import Fore, Back, Style
from interfaceNormalMode import mode_normal # Importation des modes de jeu

colorama.init()

class Sudoku:
    def __init__(self, size: int = 9):
        self.size = size
        self.grid = [[0 for _ in range(size)] for _ in range(size)]
        self.box_size = int(size ** 0.5)

    def print_grid(self):
        """Affiche la grille de manière formatée"""
        for i in range(self.size):
            if i % self.box_size == 0 and i != 0:
                print(Fore.LIGHTBLUE_EX + "-" * (self.size * 2 + self.box_size) + Fore.RESET)
            for j in range(self.size):
                if j % self.box_size == 0 and j != 0:
                    print(Fore.LIGHTBLUE_EX + "|", end=" " + Fore.RESET)
                print(self.grid[i][j] if self.grid[i][j] != 0 else ".", end=" ")
            print()

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

        # Vérifier la boîte
        box_x = col // self.box_size
        box_y = row // self.box_size
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

    def generate(self, difficulty: str = "medium"):
        """Génère une nouvelle grille avec une difficulté spécifiée"""
        # 1. Générer une grille complète
        self.solve_recursive()

        # 2. Définir le nombre de cases à retirer en fonction de la difficulté
        difficulties = {
            "easy": 35,
            "medium": 45,
            "hard": 55
        }
        cells_to_remove = difficulties.get(difficulty, 45)

        # 3. Supprimer des chiffres aléatoirement tout en conservant une seule solution
        positions = [(i, j) for i in range(self.size) for j in range(self.size)]
        random.shuffle(positions)

        for _ in range(cells_to_remove):
            row, col = positions.pop()
            self.grid[row][col] = 0

def afficher_menu_principal():
    """
    Affiche le menu principal du jeu.
    """
    text = "=== Bienvenue dans The Great Sudoku Solver ==="
    formatted_text = Back.WHITE + Fore.LIGHTBLUE_EX + text + Style.RESET_ALL

    print("\n" + formatted_text + "\n")
    print("1. Mode Normal (Jeu avec grille générée)")
    print("2. Mode Solver (Générer et résoudre une nouvelle grille)")
    print("3. Mode Sandbox (Créez votre propre grille)")
    print("4. Quitter")
    
def main():
    """
    Permet à l'utilisateur de choisir un mode.
    """
    continue_program = True
    
    while continue_program:
        afficher_menu_principal()
        choice = input("\nVotre choix (1-4): ")

        if choice == "1":
            mode_normal()  # Redirige vers le mode normal du jeu
            
        elif choice == "2":
            print("\nChoisissez la difficulté:")
            print("1. Facile")
            print("2. Moyen")
            print("3. Difficile")

            diff_choice = input("\nVotre choix (1-3): ")
            difficulty = {
                "1": "easy",
                "2": "medium",
                "3": "hard"
            }.get(diff_choice, "medium")

            sudoku = Sudoku()
            print("\nGénération de la grille...")
            sudoku.generate(difficulty)

            print("\nGrille générée:")
            sudoku.print_grid()

            input("\nAppuyez sur Entrée pour voir la solution...")

            start_time = time.time()
            if sudoku.solve_recursive():
                end_time = time.time()
                print("\nSolution trouvée en {:.2f} secondes:".format(end_time - start_time))
                sudoku.print_grid()
            else:
                print("\nErreur: Aucune solution trouvée !")

        elif choice == "3":
            sudoku = Sudoku()
            print("\nEntrez la grille ligne par ligne (utilisez 0 ou . pour les cases vides)")
            print("Exemple: 5 3 0 0 7 0 0 0 0")

            for i in range(9):
                while True:
                    try:
                        line = input(f"Ligne {i+1}: ").replace(".", "0")
                        numbers = [int(x) for x in line.split()]
                        if len(numbers) != 9:
                            raise ValueError
                        if not all(0 <= x <= 9 for x in numbers):
                            raise ValueError
                        sudoku.grid[i] = numbers
                        break
                    except ValueError:
                        print("Erreur: veuillez entrer 9 chiffres entre 0 et 9")

            print("\nGrille entrée:")
            sudoku.print_grid()

            start_time = time.time()
            if sudoku.solve_recursive():
                end_time = time.time()
                print("\nSolution trouvée en {:.2f} secondes:".format(end_time - start_time))
                sudoku.print_grid()
            else:
                print("\nAucune solution trouvée!")

        elif choice == "4":
            print(Back.WHITE + Fore.LIGHTBLUE_EX + "\nMerci d'avoir utilisé The Great Sudoku Solver!\n" + Fore.RESET + Back.RESET)
            continue_program = False

        else:
            print(Fore.RED +"\nChoix invalide, veuillez réessayer."+ Fore.RESET)

if __name__ == "__main__":
    main()
