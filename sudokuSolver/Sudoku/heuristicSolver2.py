import copy
import random
from typing import List, Tuple, Dict, Set, Optional

# Type aliases for clarity
Board = List[List[int]]
Possibilities = Dict[Tuple[int, int], Set[int]]

class SudokuHeuristicSolver:
    def __init__(self, use_randomization: bool = False):
        """
        Initialize the heuristic Sudoku solver.
        
        Args:
            use_randomization: If True, shuffle candidate values (simulates LCV randomness)
        """
        self.use_randomization = use_randomization
        self.solved = False
        self.solution: Optional[Board] = None

    def solve(self, board: Board) -> Tuple[bool, Optional[Board]]:
        """
        Solve the Sudoku puzzle using MRV + constraint propagation + backtracking.
        
        Args:
            board: 9x9 grid with 0s for empty cells
            
        Returns:
            (solved: bool, solution: Board or None)
        """
        # Make a deep copy to avoid modifying input
        board = copy.deepcopy(board)
        
        # Initialize possibilities for empty cells
        possibilities = self._initialize_possibilities(board)
        
        # Start recursive solving
        self.solved, self.solution = False, None
        success = self._heuristics(board, possibilities)
        
        return success, self.solution

    def _initialize_possibilities(self, board: Board) -> Possibilities:
        """
        Initialize possible values for each empty cell.
        """
        possibilities: Possibilities = {}
        
        # Initialize empty cells with {1..9}
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    possibilities[(row, col)] = set(range(1, 10))
        
        # Remove values based on pre-filled cells
        for row in range(9):
            for col in range(9):
                if board[row][col] != 0:
                    value = board[row][col]
                    affected = self._get_affected_cells(row, col)
                    for r, c in affected:
                        if (r, c) in possibilities:
                            possibilities[(r, c)].discard(value)
        
        return possibilities

    def _get_affected_cells(self, row: int, col: int) -> Set[Tuple[int, int]]:
        """
        Get all cells affected by placing a number at (row, col).
        """
        affected = set()
        
        # Same row
        for c in range(9):
            if c != col:
                affected.add((row, c))
        
        # Same column
        for r in range(9):
            if r != row:
                affected.add((r, col))
        
        # Same 3x3 box
        box_row = 3 * (row // 3)
        box_col = 3 * (col // 3)
        for r in range(box_row, box_row + 3):
            for c in range(box_col, box_col + 3):
                if (r, c) != (row, col):
                    affected.add((r, c))
        
        return affected

    def _is_valid_move(self, board: Board, row: int, col: int, num: int) -> bool:
        """
        Check if placing 'num' at (row, col) is valid.
        """
        # Check row
        for x in range(9):
            if board[row][x] == num:
                return False
        
        # Check column
        for x in range(9):
            if board[x][col] == num:
                return False
        
        # Check 3x3 box
        box_row = 3 * (row // 3)
        box_col = 3 * (col // 3)
        for r in range(box_row, box_row + 3):
            for c in range(box_col, box_col + 3):
                if board[r][c] == num:
                    return False
        
        return True

    def _find_most_constrained_cell(self, possibilities: Possibilities) -> Tuple[int, int, List[int]]:
        """
        Find cell with Minimum Remaining Values (MRV).
        Returns (-1, -1, []) if no empty cells.
        """
        if not possibilities:
            return -1, -1, []
        
        min_count = 10
        best_row, best_col = -1, -1
        best_values: List[int] = []
        
        for (row, col), values in possibilities.items():
            count = len(values)
            if count < min_count:
                min_count = count
                best_row, best_col = row, col
                best_values = list(values)
        
        return best_row, best_col, best_values

    def solve_with_performance_tracking(self, board: Board, possibilities: Possibilities) -> bool:
        """
        Main recursive heuristic function with MRV and constraint propagation.
        """
        # Find most constrained cell
        row, col, values = self._find_most_constrained_cell(possibilities)
        
        # If no empty cells, puzzle is solved
        if row == -1 and col == -1:
            self.solved = True
            self.solution = copy.deepcopy(board)
            return True
        
        # Optional: randomize value order (simulates LCV exploration)
        if self.use_randomization:
            random.shuffle(values)
        
        cell_coord = (row, col)
        
        # Try each possible value
        for num in values:
            if self._is_valid_move(board, row, col, num):
                # Place the number
                board[row][col] = num
                
                # Make a deep copy of possibilities
                updated_poss = copy.deepcopy(possibilities)
                del updated_poss[cell_coord]
                
                # Propagate constraints
                affected = self._get_affected_cells(row, col)
                for r, c in affected:
                    if (r, c) in updated_poss:
                        updated_poss[(r, c)].discard(num)
                        # Early failure detection: if any cell has no possibilities
                        if not updated_poss[(r, c)]:
                            board[row][col] = 0
                            continue
                
                # Recurse
                if self._heuristics(board, updated_poss):
                    return True
                
                # Backtrack
                board[row][col] = 0
        
        # Restore possibilities for this cell on failure
        possibilities[cell_coord] = set(values)
        return False


# Helper function to print board
def print_board(board: Board):
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("-" * 21)
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("| ", end="")
            print(board[i][j] if board[i][j] != 0 else ".", end=" ")
        print()
    print()

