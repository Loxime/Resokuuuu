import sys
import time
import colorama
from colorama import Fore, Back, Style
from typing import List, Optional
from copy import deepcopy
from solver import SudokuSolver
from generator import SudokuGenerator
from interfaceNormalMode import mode_normal

colorama.init()

class Sudoku:
    def __init__(self, size: int = 9):
        if size not in [4, 9, 16]:  
            raise ValueError("Seules les tailles 4x4, 9x9 et 16x16 sont supportées.")
        
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

    def generate(self, difficulty: str = "medium"):
        """Génère une nouvelle grille avec une difficulté spécifiée"""
        generator = SudokuGenerator(self.size)
        self.grid = generator.generate(difficulty)

def afficher_menu_principal():
    """Affiche le menu principal du jeu."""
    text = "=== Bienvenue dans The Great Sudoku Solver ==="
    formatted_text = Back.WHITE + Fore.LIGHTBLUE_EX + text + Style.RESET_ALL

    print("\n" + formatted_text + "\n")
    print("1. Mode Normal (Jeu avec grille générée)")
    print("2. Mode Solver (Générer et résoudre une nouvelle grille)")
    print("3. Mode Sandbox (Créez votre propre grille)")
    print("4. Quitter")

def menu_solveur():
    """Affiche un menu pour choisir le solveur"""
    print("\nChoisissez un solveur :")
    print("1. Backtracking Récursif")
    print("2. Heuristique MRV")
    print("3. Backtracking Itératif")
    print("4. Forward Checking")
    print("5. Coloration de Graphe")
    print("6. Quitter")
    choix = input("Votre choix : ")
    return int(choix) if choix.isdigit() else 6

def resoudre_grille(sudoku: Sudoku, choix_solver: int, step_by_step: bool):
    """Résout la grille en fonction du solveur choisi"""
    solver = SudokuSolver(sudoku.grid, step_by_step)
    
    solvers = {
        1: solver.solve_recursive,
        2: solver.solve_mrv,
        3: solver.solve_iterative,
        4: solver.solve_forward_checking,
        5: solver.solve_graph_coloring
    }
    
    if choix_solver in solvers:
        print(f"\nRésolution avec le solveur {choix_solver}...")
        start_time = time.perf_counter()
        solved = solvers[choix_solver]()
        end_time = time.perf_counter()
        
        if solved:
            print("\nGrille résolue avec succès !")
            sudoku.print_grid()
            print(f"Temps de résolution : {end_time - start_time:.4f} secondes")
        else:
            print("\nAucune solution trouvée !")
        return solved
    else:
        print("Choix invalide.")
        return False

def afficher_benchmark(grille_initiale: List[List[int]]):
    """Affiche les résultats des benchmarks après résolution"""
    choix = input("\nVoir les résultats du benchmark des solveurs ? (o/n) : ").lower()
    if choix == 'o':
        solver = SudokuSolver(deepcopy(grille_initiale))
        results = solver.benchmark_solvers()
        print("\n=== Benchmark des Solveurs ===")
        for method, result in results.items():
            print(f"{method.capitalize()} : {result['time']:.4f} sec - Solution trouvée : {'Oui' if result['solved'] else 'Non'}")

def main():
    """Permet à l'utilisateur de choisir un mode."""
    continuer = True
    
    while continuer:
        afficher_menu_principal()
        choice = input("\nVotre choix (1-4): ")

        if choice == "1":
            mode_normal() 
            
        elif choice == "2":
            size = None
            while size not in [4, 9, 16]:
                try:
                    size = int(input("Choisissez la taille de la grille (4, 9, 16) : ").strip())
                except ValueError:
                    size = None
                if size not in [4, 9, 16]:
                    print("Erreur : Veuillez entrer 4, 9 ou 16.")
            
            print("\nChoisissez la difficulté:")
            print("1. Facile")
            print("2. Moyen")
            print("3. Difficile")

            diff_choice = input("\nVotre choix (1-3): ")
            difficulty = {"1": "easy", "2": "medium", "3": "hard"}.get(diff_choice, "medium")

            sudoku = Sudoku(size)
            print("\nGénération de la grille...")
            sudoku.generate(difficulty)

            print("\nGrille générée:")
            sudoku.print_grid()

            input("\nAppuyez sur Entrée pour voir la solution...")

            grille_initiale = deepcopy(sudoku.grid)
            choix_solver = menu_solveur()
            if choix_solver != 6:
                step_by_step = input("\nVoulez-vous voir la résolution étape par étape ? (o/n) : ").lower() == 'o'
                solved = resoudre_grille(sudoku, choix_solver, step_by_step)
                if solved:
                    afficher_benchmark(grille_initiale)

        elif choice == "3":
            size = 9
            sudoku = Sudoku(size)
            print("\nEntrez la grille ligne par ligne (utilisez 0 ou . pour les cases vides)")

            for i in range(size):
                valid_input = False
                while not valid_input:
                    try:
                        line = input(f"Ligne {i+1}: ").replace(".", "0")
                        numbers = [int(x) for x in line.split()]
                        if len(numbers) != size or any(x < 0 or x > size for x in numbers):
                            raise ValueError
                        sudoku.grid[i] = numbers
                        valid_input = True
                    except ValueError:
                        print(f"Erreur: veuillez entrer {size} chiffres entre 0 et {size}.")

            print("\nGrille entrée:")
            sudoku.print_grid()

            grille_initiale = deepcopy(sudoku.grid)
            choix_solver = menu_solveur()
            if choix_solver != 6:
                step_by_step = input("\nVoulez-vous voir la résolution étape par étape ? (o/n) : ").lower() == 'o'
                solved = resoudre_grille(sudoku, choix_solver, step_by_step)
                if solved:
                    afficher_benchmark(grille_initiale)

        elif choice == "4":
            print(Back.WHITE + Fore.LIGHTBLUE_EX + "\nMerci d'avoir utilisé The Great Sudoku Solver!\n" + Fore.RESET + Back.RESET)
            continuer = False

        else:
            print(Fore.RED + "\nChoix invalide, veuillez réessayer." + Fore.RESET)

if __name__ == "__main__":
    main()
