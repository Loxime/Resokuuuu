from typing import List, Tuple, Optional, Dict
import time
import os
from collections import deque

class SudokuSolver:
    def __init__(self, grid: List[List[int]], step_by_step: bool = False):
        self.grid = grid
        self.size = len(grid)
        self.box_size = int(self.size ** 0.5)
        self.step_by_step = step_by_step
        self.graph = self.build_graph()

    def build_graph(self) -> Dict[Tuple[int, int], List[Tuple[int, int]]]:
        """Construit la représentation en graphe du Sudoku (chaque cellule est un nœud)."""
        graph = {}
        for row in range(self.size):
            for col in range(self.size):
                node = (row, col)
                neighbors = []

                for c in range(self.size):
                    if c != col:
                        neighbors.append((row, c))
                for r in range(self.size):
                    if r != row:
                        neighbors.append((r, col))
                box_row = (row // self.box_size) * self.box_size
                box_col = (col // self.box_size) * self.box_size
                for i in range(self.box_size):
                    for j in range(self.box_size):
                        cell = (box_row + i, box_col + j)
                        if cell != node and cell not in neighbors:
                            neighbors.append(cell)
                graph[node] = neighbors
        return graph

    def visualize_graph(self):
        """Visualise le graphe du Sudoku à l'aide de NetworkX et matplotlib en mode non bloquant."""
        import networkx as nx
        import matplotlib.pyplot as plt

        G = nx.Graph()
        for node, neighbors in self.graph.items():
            G.add_node(node)
            for neighbor in neighbors:
                if not G.has_edge(node, neighbor):
                    G.add_edge(node, neighbor)
        
        pos = nx.spring_layout(G, seed=42)  
        plt.figure(figsize=(8, 8))
        nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=500)
        plt.title("Représentation en Graphe du Sudoku")
        plt.show(block=False)
        plt.pause(10) 
        plt.close()


    def is_valid(self, num: int, pos: Tuple[int, int]) -> bool:
        """Vérifie si num peut être placé à pos sans violer les contraintes du Sudoku."""
        row, col = pos
        if num in self.grid[row]:
            return False
        if any(self.grid[i][col] == num for i in range(self.size)):
            return False
        start_row = (row // self.box_size) * self.box_size
        start_col = (col // self.box_size) * self.box_size
        for i in range(start_row, start_row + self.box_size):
            for j in range(start_col, start_col + self.box_size):
                if self.grid[i][j] == num:
                    return False
        return True

    def find_empty(self) -> Optional[Tuple[int, int]]:
        """Retourne la première case vide (0) trouvée ou None si la grille est complète."""
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == 0:
                    return (i, j)
        return None

    def solve_recursive(self) -> bool:
        """Résout le Sudoku par backtracking récursif."""
        empty = self.find_empty()
        if not empty:
            return True
        row, col = empty

        for num in range(1, self.size + 1):
            if self.is_valid(num, (row, col)):
                self.grid[row][col] = num
                if self.step_by_step:
                    self.print_grid()
                if self.solve_recursive():
                    return True
                self.grid[row][col] = 0
        return False

    def solve_mrv(self) -> bool:
        """Résout le Sudoku en utilisant l'heuristique MRV (Minimum Remaining Values)."""
        empty = self.find_empty()
        if not empty:
            return True

        min_options = self.size + 1
        best_cell = None
        best_values = set()

        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == 0:
                    options = {num for num in range(1, self.size + 1) if self.is_valid(num, (i, j))}
                    if len(options) < min_options:
                        min_options = len(options)
                        best_cell = (i, j)
                        best_values = options

        if best_cell is None:
            return True

        row, col = best_cell
        for num in best_values:
            self.grid[row][col] = num
            if self.step_by_step:
                self.print_grid()
            if self.solve_mrv():
                return True
            self.grid[row][col] = 0
        return False

    def solve_iterative(self) -> bool:
        """Résout le Sudoku de manière itérative à l'aide d'une pile."""
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
        """Résout le Sudoku en utilisant l'heuristique Forward Checking."""
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
        """Vérifie pour chaque case vide qu'il existe au moins une valeur possible."""
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == 0:
                    if not {num for num in range(1, self.size + 1) if self.is_valid(num, (i, j))}:
                        return False
        return True

    def solve_graph_coloring(self) -> bool:
        """
        Résout le Sudoku en utilisant un algorithme de coloration de graphe.
        Avant de démarrer, affiche le graphe du Sudoku à l'aide de NetworkX.
        """
        self.visualize_graph()

        colors = {cell: 0 for cell in self.graph}

        def is_safe(node, color):
            """Vérifie si l'affectation de 'color' à 'node' est sûre."""
            return all(colors[neighbor] != color for neighbor in self.graph[node])

        def color_graph(node_index):
            if node_index == len(self.graph):
                return True

            node = list(self.graph.keys())[node_index]
            row, col = node

            if self.grid[row][col] != 0:
                return color_graph(node_index + 1)

            for num in range(1, self.size + 1):
                if is_safe(node, num):
                    colors[node] = num
                    self.grid[row][col] = num
                    if self.step_by_step:
                        self.print_grid()
                    if color_graph(node_index + 1):
                        return True
                    colors[node] = 0
                    self.grid[row][col] = 0
            return False

        return color_graph(0)

    def print_grid(self):
        """Affiche la grille de Sudoku et fait une pause pour le mode pas à pas."""
        os.system('cls' if os.name == 'nt' else 'clear')
        for i in range(self.size):
            if i % self.box_size == 0 and i != 0:
                print("-" * (self.size * 2 + self.box_size))
            for j in range(self.size):
                if j % self.box_size == 0 and j != 0:
                    print("|", end=" ")
                print(self.grid[i][j] if self.grid[i][j] != 0 else ".", end=" ")
            print()
        time.sleep(0.3)

    def benchmark_solvers(self) -> dict:
        """Compare les performances des différents solveurs."""
        results = {}
        original_grid = [row[:] for row in self.grid]

        solvers = {
            "recursive": self.solve_recursive,
            "mrv": self.solve_mrv,
            "iterative": self.solve_iterative,
            "forward_checking": self.solve_forward_checking,
            "graph_coloring": self.solve_graph_coloring
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
