import random  
import copy  

def is_valid_move(grid, row, col, num):  
    # Check row  
    if num in grid[row]:  
        return False  
    
    # Check column  
    if num in [grid[i][col] for i in range(9)]:  
        return False  
    
    # Check 3x3 box  
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)  
    for i in range(3):  
        for j in range(3):  
            if grid[start_row + i][start_col + j] == num:  
                return False  
    
    return True  

def solve_sudoku(grid):  
    for row in range(9):  
        for col in range(9):  
            if grid[row][col] == 0:  
                # Shuffle possible numbers  
                nums = list(range(1, 10))  
                random.shuffle(nums)  
                
                for num in nums:  
                    if is_valid_move(grid, row, col, num):  
                        grid[row][col] = num  
                        
                        if solve_sudoku(grid):  
                            return True  
                        
                        grid[row][col] = 0  
                
                return False  
    return True  

def count_solutions(grid):  
    solutions = [0]  
    
    def backtrack(grid):  
        if solutions[0] > 1:  
            return  
        
        for row in range(9):  
            for col in range(9):  
                if grid[row][col] == 0:  
                    for num in range(1, 10):  
                        if is_valid_move(grid, row, col, num):  
                            grid[row][col] = num  
                            
                            if all(0 not in row for row in grid):  
                                solutions[0] += 1  
                                if solutions[0] > 1:  
                                    return  
                            
                            backtrack(grid)  
                            
                            grid[row][col] = 0  
                    return  
        return  

    backtrack(grid)  
    return solutions[0]  

def generate_sudoku(difficulty=30):  
    # Create an empty grid  
    grid = [[0 for _ in range(9)] for _ in range(9)]  
    
    # Solve the empty grid  
    solution = solve_sudoku(grid)  
    
    # Randomize positions for removal  
    positions = [(row, col) for row in range(9) for col in range(9)]  
    random.shuffle(positions)  
    
    # Create a copy of the solved grid  
    puzzle = [row[:] for row in grid]  
    
    # Try to remove numbers  
    removed = 0  
    for row, col in positions:  
        if removed >= 81 - difficulty:  
            break  
        
        # Store the original value  
        temp = puzzle[row][col]  
        puzzle[row][col] = 0  
        
        # Check if removal creates multiple solutions  
        grid_copy = [row[:] for row in puzzle]  
        if count_solutions(grid_copy) > 1:  
            # If multiple solutions, put the number back  
            puzzle[row][col] = temp  
        else:  
            removed += 1  
    
    return puzzle, solution

# Generate and print a Sudoku puzzle  
def print_sudoku(grid):  
    for row in grid:  
        print(' '.join(str(num) if num != 0 else '.' for num in row))  

# Generate and print multiple Sudoku puzzles  
# for i in range(3):  
#     print(f"\nSudoku Puzzle {i+1}:")  
#     sudoku_puzzle = generate_sudoku(difficulty=40)  # Adjust difficulty (30-50 recommended)  
#     print_sudoku(sudoku_puzzle)  
#     print("\n")