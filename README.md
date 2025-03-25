# Sudoku-Solver
A Django-based web application that provides a comprehensive Sudoku gaming experience, featuring gameplay, puzzle generation, solving capabilities, and user management.

This project aims to serve as a learning tool to help users understand and analyze different Sudoku-solving techniques.

![SudokuSolver](https://github.com/SafalNarsingh/Sudoku-Solver/blob/0170b80f32815371ea2d7260fc5cb594e9cb1795/imgs/Homepage.png)


## Table of Contents  

1. [Screenshots](#screenshots)  
2. [Features](#features)  
3. [Usage/Examples](#usageexamples) 
4. [Algorithms](#algorithms)
4. [Dependencies](#dependencies)  
5. [Troubleshooting](#troubleshooting)  
6. [Supported Operatorions](#supported-operations)  
7. [Contributors](#contributors)  
8. [To-Do List](#to-do-list)  


## Screenshots

![HomePage](https://github.com/SafalNarsingh/Sudoku-Solver/blob/0170b80f32815371ea2d7260fc5cb594e9cb1795/imgs/Homepage.png)

![Login](https://github.com/SafalNarsingh/Sudoku-Solver/blob/0170b80f32815371ea2d7260fc5cb594e9cb1795/imgs/login.png)

![Level](https://github.com/SafalNarsingh/Sudoku-Solver/blob/0170b80f32815371ea2d7260fc5cb594e9cb1795/imgs/level.png)

![Play](https://github.com/SafalNarsingh/Sudoku-Solver/blob/0170b80f32815371ea2d7260fc5cb594e9cb1795/imgs/play.png)

![Solver](https://github.com/SafalNarsingh/Sudoku-Solver/blob/0170b80f32815371ea2d7260fc5cb594e9cb1795/imgs/solver.png)

![Solved](https://github.com/SafalNarsingh/Sudoku-Solver/blob/0170b80f32815371ea2d7260fc5cb594e9cb1795/imgs/solved.png)

![Profile](https://github.com/SafalNarsingh/Sudoku-Solver/blob/e94815614de0827b1f1f7808198d8dfc86f4a193/imgs/profile.png)


## Features

### <u>👤 User Authentication & Profile Management</u>
Users can sign up, log in, and log out securely. Each user has a profile that tracks their high scores and game progress. Users can change their username or delete their profile if they wish.

### <u> 🧠 Difficulty Levels </u>
Players can choose from multiple difficulty levels:
Beginner 
Easy
Medium
Hard
Extreme

The difficulty level affects the number of pre-filled numbers on the board.

### <u> 🧐 Sudoku Solver </u> 
Users can manually input a puzzle or generate a new one.
The solver uses two different algorithms:

- Backtracking Algorithm – A traditional recursive approach.

- Heuristic Solver – A smarter, faster approach for solving Sudoku puzzles.

The solver compares both methods and provides time estimates.

### <u> 🎮 Scoring & Performance Tracking </u>
The app tracks the best scores for each user.
Score calculation is based on:
- Number of correct inputs: The player is awarded 40 points for every correct input on the puzzle


### <u> ⌛ Game Pausing & Resuming </u>
Users can pause a game and resume it later without losing progress.

### <u> 📱 Mobile-Friendly UI </u>
The web app is fully responsive and optimized for mobile devices.
Touch-friendly controls make playing Sudoku easy on smartphones and tablets.

For instance, below you can view the example of the web application opened through an android phone:

<div style="display: flex; justify-content: space-between;">  
    <img src="https://github.com/SafalNarsingh/Sudoku-Solver/blob/8da06b1f1bc090e0f396f061847d6c4f559d7096/imgs/home_mobile.jpg" alt="Home_Mobile" style="width: 24%; height: 500px; object-fit: cover;">  
    <img src="https://github.com/SafalNarsingh/Sudoku-Solver/blob/8da06b1f1bc090e0f396f061847d6c4f559d7096/imgs/level_mobile.jpg" alt="Level_Mobile" style="width: 24%; height: 500px; object-fit: cover;">  
    <img src="https://github.com/SafalNarsingh/Sudoku-Solver/blob/8da06b1f1bc090e0f396f061847d6c4f559d7096/imgs/solver_mobile.jpg" alt="Solver_Mobile" style="width: 24%; height: 500px; object-fit: cover;">  
    <img src="https://github.com/SafalNarsingh/Sudoku-Solver/blob/8da06b1f1bc090e0f396f061847d6c4f559d7096/imgs/solved_mobile.jpg" alt="Solved_Mobile" style="width: 24%; height: 500px; object-fit: cover;">  
</div>  


## Usage/Examples

### <u> Playing Sudoku </u>
1.  Log in to your account.
2.  Select a difficulty level from the homepage.
3.  The Sudoku game board will load based on the selected difficulty.
4.  Click or tap on an empty cell to enter a number.
5.   Click "Save Game" to store your progress.

### <u>  Solving a Sudoku Puzzle </u>
- Go to the Solver page.
- Manually enter a Sudoku puzzle.
- Click "Solve", and the app will display the solution instantly along with time analysis of backtracking and heuristic algorithm.



## Algorithms

### <u> Backtracking Algorithm </u>
The Backtracking Algorithm is a recursive brute-force approach used to solve Sudoku puzzles by trying every possible number in each empty cell until a valid solution is found. It follows a Depth-First Search (DFS) strategy, starting from the first empty cell and attempting to place numbers from 1 to 9 while checking if the placement violates Sudoku rules. If an invalid placement is encountered, it backtracks by removing the last placed number and trying the next possible value. While this method guarantees a solution if one exists, it can be computationally expensive, especially for complex puzzles, as it relies on trial and error.

### <u> Heuristic Algorithm </u>
The Heuristic Algorithm applies intelligent rule-based techniques to solve Sudoku more efficiently. Instead of brute-force searching, it uses constraint propagation, which eliminates impossible values early based on existing numbers in rows, columns, and boxes. Additionally, it implements Most Constrained Variable (MRV) Heuristic, prioritizing solving the cells with the fewest possible options first, and Least Constraining Value (LCV) Heuristic, selecting numbers that restrict future moves the least. Forward checking is also applied to dynamically track possibilities and prevent dead ends. This approach significantly improves solving speed compared to backtracking, making it ideal for difficult puzzles. However, while heuristic methods can solve most Sudoku puzzles quickly, they may require backtracking support for extremely challenging grids.

By combining these two approaches, the Sudoku solver in this project allows for performance comparison, measuring execution times for both methods to determine which one is more efficient for a given puzzle.


## Dependencies
The project relies on the following dependencies:
- Python
- Django (for backend logic and user management)
- Django authentication system (for login/logout features)
- JSON Processing (for game state storage and retrieval)
- HTML, CSS, JavaScript (for UI and interactivity)


## Installation

To install and run the Sudoku Solver locally, follow these steps:
1. Clone the repository on your local environment:
```s
git clone https://github.com/SafalNarsingh/Sudoku-Solver
```

2. Install dependencies using:
```s
pip install -r requirements.txt
```

3. Locate the the root directory and run the following command:
```s
py manage.py runserver
```

Your server should be hosted locally within the given address. Open and enjoy.

Alternatively, 
You can run the web app using the following link:
https://solversudoku.vercel.app/


## Troubleshooting
### <u> ❗ Login Issues </u>
Ensure your username is correct and not already taken.
Admin users cannot log in through the standard user portal.

### <u> ❗ Game Not Saving </u>
Make sure you are logged in before trying to save the game.
Check the server logs for any errors.

### <u> ❗ Sudoku Solver Not Working </u>
Ensure the input board is correctly formatted.
If no solution is found, verify that the puzzle is valid and solvable.

## Supported Operations
- <u> User Management: </u> 
    - Login, Logout, Change Username, Delete Profile

- <u> Game Operations: </u>
    - Start Game, Set Difficulty, Save/Load Game State, Solve Sudoku

## To-Do List


- [ ] Enhance play page for mobile rendering 
- [ ] Fix the save game state function (not working currently)
- [ ] Add real-time multiplayer Sudoku.
- [ ] Enhance score tracking with leaderboards.
- [ ] Implement hints and undo functionality.
- [ ] Add more algorithms for faster performance and better understanding of more sudoku solving algorithms.

## Contributors

Apekshya Bhattarai <br>
Salina Nakarmni <br>
Pooja Pathak <br>
Safal Narshing Shrestha <br>
Dinisha Uprety <br>

> Last updated by Safal Narshing Shrestha on March 25, 2025, 17:24. </br> Copyright © 2025 Apekshya Bhattarai, Salina Nakarmni, Pooja Pathak, Safal Narshing Shrestha, Dinisha Uprety. All rights reserved.

##
