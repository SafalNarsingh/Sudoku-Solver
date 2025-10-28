from copy import deepcopy
import time
from .heuristicSolver2 import solve_with_performance_tracking
from .recursiveBacktracking import solve_backtracking
def solve_with_comparison(board):
    """Compare both solving methods on identical boards"""
    # Create deep copies of the board for each solver
    board_heuristic = deepcopy(board)
    board_backtrack = deepcopy(board)
    
    # Run heuristic solver (returns a dict with keys like 'solved' and 'solution')
    start_time = time.time()
    heuristic_result = solve_with_performance_tracking(board_heuristic)
    # normalize result
    heuristic_success = bool(heuristic_result.get('solved', False)) if isinstance(heuristic_result, dict) else bool(heuristic_result)
    # prefer solver-provided timing/solution when available
    heuristic_time = (heuristic_result.get('time_taken', time.time() - start_time) if isinstance(heuristic_result, dict) else (time.time() - start_time)) * 1000
    heuristic_solution = heuristic_result.get('solution', board_heuristic) if isinstance(heuristic_result, dict) else board_heuristic
    
    # Run backtracking solver
    start_time = time.time()
    backtrack_success = solve_backtracking(board_backtrack)
    backtrack_time = (time.time() - start_time) * 1000
    
    # Use the heuristic solution if both were successful
    final_solution = board_heuristic
    if heuristic_success and backtrack_success:
        # prefer explicit solution returned by heuristic solver when present
        final_solution = heuristic_solution

    return (heuristic_success and backtrack_success), final_solution, heuristic_time, backtrack_time

# def solve_with_optimized_heuristic(board):
    possibilities = initialize_possibilities(board)
    return solve_heuristic_recursive(board, possibilities)

# def solve_heuristic_recursive(board, possibilities):
    row, col, possible_values = find_most_constrained_cell(possibilities)
    
    if row == -1:  # No empty cells left
        return True
        
    if not possible_values:  # No valid moves
        return False
    
    saved_possibilities = {k: v.copy() for k, v in possibilities.items()}
    
    for value in possible_values:
        board[row][col] = value
        del possibilities[(row, col)]
        
        # Update affected cells' possibilities
        affected_cells = get_affected_cells(row, col)
        for affected_row, affected_col in affected_cells:
            if (affected_row, affected_col) in possibilities:
                possibilities[(affected_row, affected_col)].discard(value)
        
        if solve_heuristic_recursive(board, possibilities):
            return True
            
        # Backtrack
        board[row][col] = 0
        possibilities.clear()
        possibilities.update(saved_possibilities)
    
    return False

# def solve_backtracking(board):
    empty = find_empty(board)
    if not empty:
        return True
        
    row, col = empty
    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num
            if solve_backtracking(board):
                return True
            board[row][col] = 0
            
    return False

# Helper functions
# def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None

# def is_valid(board, row, col, num):
    # Check row
    if num in board[row]:
        return False
        
    # Check column
    if num in [board[i][col] for i in range(9)]:
        return False
        
    # Check 3x3 box
    box_row, box_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            if board[i][j] == num:
                return False
                
    return True

# def get_affected_cells(row, col):
    affected = set()
    
    # Add row cells
    for c in range(9):
        if c != col:
            affected.add((row, c))
    
    # Add column cells
    for r in range(9):
        if r != row:
            affected.add((r, col))
    
    # Add box cells
    box_row, box_col = 3 * (row // 3), 3 * (col // 3)
    for r in range(box_row, box_row + 3):
        for c in range(box_col, box_col + 3):
            if (r, c) != (row, col):
                affected.add((r, c))
                
    return affected

# def initialize_possibilities(board):
    possibilities = {}
    
    # Initialize empty cells with all possibilities
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                possibilities[(row, col)] = set(range(1, 10))
    
    # Remove possibilities based on existing numbers
    for row in range(9):
        for col in range(9):
            if board[row][col] != 0:
                value = board[row][col]
                affected_cells = get_affected_cells(row, col)
                for r, c in affected_cells:
                    if (r, c) in possibilities:
                        possibilities[(r, c)].discard(value)
    
    return possibilities

# def find_most_constrained_cell(possibilities):
    if not possibilities:
        return -1, -1, []
        
    min_possibilities = 10
    best_cell = (-1, -1)
    best_values = []
    
    for (row, col), possible_values in possibilities.items():
        num_possibilities = len(possible_values)
        if num_possibilities < min_possibilities:
            min_possibilities = num_possibilities
            best_cell = (row, col)
            best_values = possible_values
            
    return best_cell[0], best_cell[1], list(best_values)