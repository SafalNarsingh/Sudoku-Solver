import time  
import random  
import copy
from typing import List, Dict, Set, Tuple  

def get_affected_cells(row: int, col: int) -> Set[Tuple[int, int]]:  
    """  
    Returns set of cells that would be affected by placing a number at (row, col)  
    
    Args:  
        row (int): Row index  
        col (int): Column index  
    
    Returns:  
        Set of affected cell coordinates  
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
    box_row, box_col = 3 * (row // 3), 3 * (col // 3)  
    for r in range(box_row, box_row + 3):  
        for c in range(box_col, box_col + 3):  
            if (r, c) != (row, col):  
                affected.add((r, c))  
                
    return affected  

def initialize_possibilities(board: List[List[int]]) -> Dict[Tuple[int, int], Set[int]]:  
    """  
    Create initial dictionary of possibilities for all empty cells  
    
    Args:  
        board (List[List[int]]): 9x9 Sudoku grid  
    
    Returns:  
        Dictionary of cell coordinates and possible values  
    """  
    possibilities = {}  
    
    # Set all empty cells to have all possibilities  
    for row in range(9):  
        for col in range(9):  
            if board[row][col] == 0:  
                possibilities[(row, col)] = set(range(1, 10))  
    
    # Remove possibilities based on existing numbers  
    for row in range(9):  
        for col in range(9):  
            if board[row][col] != 0:  
                value = board[row][col]  
                # Remove this value from all affected cells  
                for r, c in get_affected_cells(row, col):  
                    if (r, c) in possibilities:  
                        possibilities[(r, c)].discard(value)  
    
    return possibilities  

def find_most_constrained_cell(possibilities: Dict[Tuple[int, int], Set[int]]) -> Tuple[int, int, List[int]]:  
    """  
    Find the empty cell with fewest possible values  
    
    Args:  
        possibilities (Dict): Dictionary of cell possibilities  
    
    Returns:  
        Tuple containing row, column, and possible values  
    """  
    if not possibilities:  # If no empty cells left  
        return -1, -1, []  
        
    # Find cell with minimum number of possibilities  
    min_possibilities = 10  
    best_cell = (-1, -1)  
    best_values = []  
    
    for (row, col), possible_values in possibilities.items():  
        if len(possible_values) < min_possibilities:  
            min_possibilities = len(possible_values)  
            best_cell = (row, col)  
            best_values = possible_values  
            
    return best_cell[0], best_cell[1], list(best_values)  


def is_valid_move(board: List[List[int]], row: int, col: int, num: int) -> bool:  
    """Check if a move is valid"""  
    # Check row and column  
    for x in range(9):  
        if board[row][x] == num or board[x][col] == num:  
            return False  
    
    # Check 3x3 box  
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)  
    for i in range(3):  
        for j in range(3):  
            if board[start_row + i][start_col + j] == num:  
                return False  
    
    return True  


def solve_sudoku(board: List[List[int]],   
                 time_limit: float = 5.0,   
                 use_randomization: bool = True) -> Dict:  
    """  
    Comprehensive Sudoku solving function  
    
    Args:  
        board (List[List[int]]): 9x9 Sudoku grid  
        time_limit (float): Maximum solving time in seconds  
        use_randomization (bool): Enable value randomization  
    
    Returns:  
        Dictionary with solving results  
    """  
    start_time = time.time()  
    original_board = [row[:] for row in board]  
    
    results = {  
        'solved': False,  
        'solution': None,  
        'time_taken': 0,  
        'error': None  
    }  
    
    def backtrack_solve_with_heuristics(board: List[List[int]], possibilities: Dict[Tuple[int, int], Set[int]]) -> bool:  
        """Recursive backtracking solver using heuristics"""  
        # Check time limit  
        if time.time() - start_time > time_limit:  
            return False  
        
        # Find most constrained cell using heuristic
        row, col, values = find_most_constrained_cell(possibilities)
        
        # If no empty cell, puzzle is solved  
        if row == -1 and col == -1:  
            results['solved'] = True  
            results['solution'] = [row[:] for row in board]  
            return True  
        
        # Randomize values if enabled
        if use_randomization:  
            random.shuffle(values)  
        
        # Create a copy of the possibilities for backtracking
        cell_coord = (row, col)
        
        # Try each possible value
        for num in values:
            if is_valid_move(board, row, col, num):
                board[row][col] = num
                
                # Remove this cell from possibilities and update affected cells
                updated_possibilities = copy.deepcopy(possibilities)
                del updated_possibilities[cell_coord]
                
                # Update possibilities for affected cells
                for r, c in get_affected_cells(row, col):
                    if (r, c) in updated_possibilities:
                        updated_possibilities[(r, c)].discard(num)
                
                if backtrack_solve_with_heuristics(board, updated_possibilities):
                    return True
                
                board[row][col] = 0  # Backtrack
        
        # No valid value found, add cell back to possibilities
        possibilities[cell_coord] = set(values)
        return False  
    
    try:  
        # Initialize possibilities for all empty cells
        initial_possibilities = initialize_possibilities(board)
        
        # Attempt to solve using heuristics
        backtrack_solve_with_heuristics(board, initial_possibilities)
    except Exception as e:  
        results['error'] = str(e)  
    finally:  
        results['time_taken'] = time.time() - start_time  
    
    return results  

# Optional: Performance measurement wrapper  
def solve_with_performance_tracking(board: List[List[int]]) -> Dict:  
    """  
    Wrapper function to track solving performance  
    
    Args:  
        board (List[List[int]]): 9x9 Sudoku grid  
    
    Returns:  
        Dictionary with detailed solving metrics  
    """  
    start_time = time.time()  
    result = solve_sudoku(board)  
    
    # Add additional performance metrics  
    result['start_time'] = start_time  
    result['end_time'] = time.time()  
    result['board'] = board  
    
    return result  

