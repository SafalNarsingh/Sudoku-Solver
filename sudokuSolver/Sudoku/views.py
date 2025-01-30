from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from .heuristicSolver2 import solve_with_optimized_heuristic
from .puzzleGenerator2 import generate_sudoku
from .models import UserInfo
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
# Create your views here.

@csrf_exempt

def index(request):  
    context = {}  
    if request.user.is_authenticated:  
        try:  
            # Retrieve the UserInfo associated with the user  
            user_info = UserInfo.objects.get(user=request.user)  
            context['high_score'] = user_info.high_score or 0
            context['username'] = request.user.username  

            print("User:", request.user)  
            print("Username:", context['username'])  
            print("High Score:", context['high_score']) 
        except UserInfo.DoesNotExist:  
            # If UserInfo doesn't exist, create it with default values
            UserInfo.objects.create(
                user=request.user, 
                username=request.user.username, 
                high_score=0
            )
            context['username'] = request.user.username  
            context['high_score'] = 0  
    return render(request, 'index.html', context)

@login_required  
def change_username(request):  
    if request.method == 'POST':  
        try:  
            # Parse JSON data  
            data = json.loads(request.body)  
            new_username = data.get('username', '').strip()  
            
            # Validate username  
            if not new_username:  
                return JsonResponse({'success': False, 'error': 'Username cannot be empty'})  
            
            # Check if username already exists  
            if User.objects.exclude(pk=request.user.pk).filter(username=new_username).exists():  
                return JsonResponse({'success': False, 'error': 'Username already exists'})  
            
            # Update user's username  
            user = request.user  
            user.username = new_username  
            user.save()  
            
            # Update UserInfo model if it exists  
            user_info, created = UserInfo.objects.get_or_create(user=user)  
            user_info.username = new_username  
            user_info.save()  
            
            return JsonResponse({  
                'success': True,   
                'username': new_username,
                'high_score': user_info.high_score or 0  # Include high score in response
            })  
        
        except Exception as e:  
            return JsonResponse({  
                'success': False,   
                'error': str(e)  
            })  
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
def delete_profile(request):
    if request.method == 'POST':
        try:
            user = request.user
            user.delete()  # This will also delete the associated profile due to CASCADE
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
def custom_logout(request):
    logout(request)
    if 'solver' in request.META.get('HTTP_REFERER', ''):
        return redirect('solver')
    return redirect('home')

def view_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        
        if not username or username.strip() == '':
            messages.error(request, 'Username cannot be empty')
            return render(request, 'Sudoku/login.html')
        
        try:
            # Check if username exists
            user = User.objects.filter(username=username.strip()).first()
            
            # If user doesn't exist, create a new non-staff user
            if not user:
                user = User.objects.create_user(
                    username=username.strip(),
                    is_staff=False
                )
            
            # Prevent staff/superuser login
            if user.is_staff:
                messages.error(request, 'Admin users cannot log in through this portal')
                return render(request, 'Sudoku/login.html')
            
            # Create or get UserInfo profile
            user_info, profile_created = UserInfo.objects.get_or_create(
                user=user,
                defaults={
                    'username': username.strip(),
                    'high_score': 0
                }
            )
            
            # Log the user in
            login(request, user)
            
            messages.success(request, 'Login successful!')
            return redirect('level')
        
        except Exception as e:
            print(f"Login error: {e}")
            messages.error(request, f'Login failed: {str(e)}')
            return render(request, 'Sudoku/login.html')
    
    return render(request, 'Sudoku/login.html')

def index_view(request):
    return render(request, 'Sudoku/index.html')

def level_view(request):
    return render(request, 'Sudoku/level.html')

def grid_view(request):
    return render(request, 'Sudoku/play.html')

# def login_view(request):
#     return render(request, 'Sudoku/login.html')

def solver_view(request):
    return render(request, 'Sudoku/solver.html')

@csrf_exempt
def sudokuGenerate(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            clues = body.get('clues',30)  # Default to 36 if not provided, but should now use sent value
            
            print(f"Received clues: {clues}")  # Debug print
            
            # base_grid = generate_base_grid()
            # shuffled_grid = shuffle_grid(base_grid)
            sudoku_puzzle, solution = generate_sudoku(clues)
            
            print(f"Generated puzzle with {clues} clues:")
            for row in sudoku_puzzle:
                print(row)
            
            return JsonResponse({'puzzle': sudoku_puzzle,'solution': solution})
        except Exception as e:
            print(f"Error generating sudoku: {e}")
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def game_view(request):
    if request.user.is_authenticated:
        game_data = UserInfo.objects.get(user=request.user)
        context = {
            'game_state': game_data.game_state,
            'time': game_data.time,
            'score': game_data.score,
        }
        return render(request, 'sudoku_game.html', context)
    return redirect('login')

def save_game_state(request):
    if request.method == 'POST' and request.user.is_authenticated:
        data = json.loads(request.body)
        game_state = data.get('game_state')
        time = data.get('time')
        score = data.get('score')
        
        game_data = UserInfo.objects.get(user=request.user)
        game_data.game_state = game_state
        game_data.time = time
        game_data.score = score
        game_data.save()
        
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@csrf_exempt
def solve_sudoku(request):
    if request.method == 'POST':
        try:
             board = [[0 for _ in range(9)] for _ in range(9)]
             for row in range(9):
                for col in range(9):
                    cell_name = f'cell_{row}_{col}'
                    value = request.POST.get(cell_name, '').strip()
                    if value and value.isdigit() and 1 <= int(value) <= 9:
                        board[row][col] = int(value)
             if solve_with_optimized_heuristic(board):
                 return JsonResponse({
                    'solved': True, 
                    'solution': board
                })
             else:
                return JsonResponse({
                'solved': False, 
                'error': 'No solution exists'
                })
        except Exception as e:
            print(f"Exception in solve_sudoku: {e}")
        return JsonResponse({
            'solved': False, 
            'error': str(e)
        })
    return JsonResponse({
        'solved': False, 
        'error': 'Invalid request method'
    })

