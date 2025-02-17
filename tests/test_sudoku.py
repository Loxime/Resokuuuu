import unittest
from sudoku.solver import SudokuSolver
from sudoku.generator import SudokuGenerator
import time

class TestSudoku(unittest.TestCase):
    def setUp(self):
        """Initialisation des grilles de test"""
        # Grille facile
        self.easy_grid = [
            [5,3,0,0,7,0,0,0,0],
            [6,0,0,1,9,5,0,0,0],
            [0,9,8,0,0,0,0,6,0],
            [8,0,0,0,6,0,0,0,3],
            [4,0,0,8,0,3,0,0,1],
            [7,0,0,0,2,0,0,0,6],
            [0,6,0,0,0,0,2,8,0],
            [0,0,0,4,1,9,0,0,5],
            [0,0,0,0,8,0,0,7,9]
        ]

        # Grille résolue correspondante
        self.solved_grid = [
            [5,3,4,6,7,8,9,1,2],
            [6,7,2,1,9,5,3,4,8],
            [1,9,8,3,4,2,5,6,7],
            [8,5,9,7,6,1,4,2,3],
            [4,2,6,8,5,3,7,9,1],
            [7,1,3,9,2,4,8,5,6],
            [9,6,1,5,3,7,2,8,4],
            [2,8,7,4,1,9,6,3,5],
            [3,4,5,2,8,6,1,7,9]
        ]

        # Grille invalide (avec conflit)
        self.invalid_grid = [
            [5,5,0,0,7,0,0,0,0],  # Deux 5 dans la même ligne
            [6,0,0,1,9,5,0,0,0],
            [0,9,8,0,0,0,0,6,0],
            [8,0,0,0,6,0,0,0,3],
            [4,0,0,8,0,3,0,0,1],
            [7,0,0,0,2,0,0,0,6],
            [0,6,0,0,0,0,2,8,0],
            [0,0,0,4,1,9,0,0,5],
            [0,0,0,0,8,0,0,7,9]
        ]

    def test_solver_recursive(self):
        """Test du solveur récursif"""
        solver = SudokuSolver(self.easy_grid)
        self.assertTrue(solver.solve_recursive())
        self.assertEqual(solver.grid, self.solved_grid)

    def test_solver_mrv(self):
        """Test du solveur MRV"""
        solver = SudokuSolver(self.easy_grid)
        self.assertTrue(solver.solve_mrv())
        self.assertEqual(solver.grid, self.solved_grid)

    def test_solver_iterative(self):
        """Test du solveur itératif"""
        solver = SudokuSolver(self.easy_grid)
        self.assertTrue(solver.solve_iterative())
        self.assertEqual(solver.grid, self.solved_grid)

    def test_invalid_grid(self):
        """Test avec une grille invalide"""
        solver = SudokuSolver(self.invalid_grid)
        self.assertFalse(solver.solve_recursive())

    def test_generator(self):
        """Test du générateur de grilles"""
        generator = SudokuGenerator()
        
        # Test de génération pour chaque niveau de difficulté
        for difficulty in ['easy', 'medium', 'hard']:
            grid = generator.generate(difficulty)
            
            # Vérifier que la grille est de la bonne taille
            self.assertEqual(len(grid), 9)
            self.assertEqual(len(grid[0]), 9)
            
            # Vérifier que les nombres sont dans la plage correcte
            for row in grid:
                for cell in row:
                    self.assertTrue(0 <= cell <= 9)
            
            # Vérifier que la grille est résolvable
            solver = SudokuSolver(grid)
            self.assertTrue(solver.solve_recursive())

    def test_unique_solution(self):
        """Test de l'unicité de la solution"""
        generator = SudokuGenerator()
        grid = generator.generate('medium')
        
        # Copier la grille
        grid_copy = [row[:] for row in grid]
        
        # Résoudre avec différentes méthodes
        solver1 = SudokuSolver(grid)
        solver2 = SudokuSolver(grid_copy)
        
        solver1.solve_recursive()
        solver2.solve_mrv()
        
        # Les solutions doivent être identiques
        self.assertEqual(solver1.grid, solver2.grid)

    def test_performance(self):
        """Test de performance des différents solveurs"""
        solver = SudokuSolver(self.easy_grid)
        results = solver.benchmark_solvers()
        
        # Vérifier que tous les solveurs trouvent une solution
        for method, result in results.items():
            self.assertTrue(result['solved'], f"Le solveur {method} n'a pas trouvé de solution")
            self.assertLess(result['time'], 1.0, f"Le solveur {method} est trop lent")

    def test_grid_validation(self):
        """Test des fonctions de validation"""
        solver = SudokuSolver(self.easy_grid)
        
        # Test de position valide
        self.assertTrue(solver.is_valid(1, (0, 2)))
        
        # Test de position invalide (même ligne)
        self.assertFalse(solver.is_valid(5, (0, 2)))
        
        # Test de position invalide (même colonne)
        self.assertFalse(solver.is_valid(6, (1, 0)))
        
        # Test de position invalide (même carré)
        self.assertFalse(solver.is_valid(3, (0, 1)))

    def test_difficulty_levels(self):
        """Test des niveaux de difficulté"""
        generator = SudokuGenerator()
        
        # Générer des grilles de différentes difficultés
        easy_grid = generator.generate('easy')
        medium_grid = generator.generate('medium')
        hard_grid = generator.generate('hard')
        
        # Compter les cases vides
        easy_empty = sum(row.count(0) for row in easy_grid)
        medium_empty = sum(row.count(0) for row in medium_grid)
        hard_empty = sum(row.count(0) for row in hard_grid)
        
        # Vérifier que la difficulté correspond au nombre de cases vides
        self.assertLess(easy_empty, medium_empty)
        self.assertLess(medium_empty, hard_empty)

if __name__ == '__main__':
    unittest.main(verbosity=2)