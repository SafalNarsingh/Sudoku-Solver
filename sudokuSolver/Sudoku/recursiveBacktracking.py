from typing import List, Optional  

def solve_sudoku_backtracking(board: List[List[int]]) -> bool:  
    """  
    Solve Sudoku using backtracking algorithm  
    
    Args:  
        board (List[List[int]]): 9x9 Sudoku grid  
    
    Returns:  
        bool: True if solved, False otherwise  
    """  
    # Find empty cell  
    empty = find_empty_cell(board)  
    if not empty:  
        return True  # Puzzle solved  
    
    row, col = empty  
    
    # Try digits 1-9  
    for num in range(1, 10):  
        if is_valid_move(board, row, col, num):  
            board[row][col] = num  
            
            # Recursive backtracking  
            if solve_sudoku_backtracking(board):  
                return True  
            
            # Backtrack if solution not found  
            board[row][col] = 0  
    
    return False  

def find_empty_cell(board: List[List[int]]) -> Optional[tuple]:  
    """  
    Find first empty cell in the board  
    
    Args:  
        board (List[List[int]]): 9x9 Sudoku grid  
    
    Returns:  
        tuple or None: (row, col) of empty cell, or None if no empty cells  
    """  
    for row in range(9):  
        for col in range(9):  
            if board[row][col] == 0:  
                return (row, col)  
    return None  

def is_valid_move(board: List[List[int]], row: int, col: int, num: int) -> bool:  
    """  
    Check if placing 'num' at (row, col) is valid  
    
    Args:  
        board (List[List[int]]): 9x9 Sudoku grid  
        row (int): Row index  
        col (int): Column index  
        num (int): Number to place  
    
    Returns:  
        bool: True if move is valid, False otherwise  
    """  
    # Check row  
    for x in range(9):  
        if board[row][x] == num and x != col:  
            return False  
    
    # Check column  
    for x in range(9):  
        if board[x][col] == num and x != row:  
            return False  
    
    # Check 3x3 box  
    box_x, box_y = 3 * (row // 3), 3 * (col // 3)  
    for i in range(box_x, box_x + 3):  
        for j in range(box_y, box_y + 3):  
            if board[i][j] == num and (i, j) != (row, col):  
                return False  
    
    return True  
