import copy
import pygame
import enum
from random import randint
from sys import exit

class Change(enum.Enum):
    reset = 0
    make_red = 1
    move_piece_from = 2
    move_piece = 3

class Game_State(enum.Enum):
    main_menu = 0
    chess = 1
    randomize = 2
    check = 3

class Pieces(enum.Enum):
    empty_space = 1
    player_pawn = 2
    player_rook = 3
    player_knight = 4
    player_bishop = 5
    player_queen = 6
    player_king = 7
    opponent_pawn = 8
    opponent_rook = 9
    opponent_knight = 10
    opponent_bishop = 11
    opponent_queen = 12
    opponent_king = 13
pygame.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Chess2")
clock = pygame.time.Clock()

# Board
board_surface = pygame.image.load("graphics/Chess Board.png")
board_surface = pygame.transform.scale(board_surface, (800, 800))
board_rect = board_surface.get_rect(topleft=(0, 0))
previous_piece_index = (0,0)
player_turn = 1
player_win = 0
opponent_win = 0
game_state = Game_State.main_menu


#Code:
#1 means empty space
#2 means player pawn
#3 means player rook
#4 means player knight
#5 means player bishop
#6 means player queen
#7 means player king
#8 means opponent pawn
#9 means opponent rook
#10 means opponent knight
#11 means opponent bishop
#12 means opponent queen
#13 means opponent king
chess_board = [[3, 4, 5, 6, 7, 5, 4, 3],
               [2, 2, 2, 2, 2, 2, 2, 2],
               [1, 1, 1, 1, 1, 1, 1, 1],
               [1, 1, 1, 1, 1, 1, 1, 1],
               [1, 1, 1, 1, 1, 1, 1, 1],
               [1, 1, 1, 1, 1, 1, 1, 1],
               [8, 8, 8, 8, 8, 8, 8, 8],
               [9, 10, 11, 12, 13, 11, 10, 9]]
start_chess_board = chess_board.copy()
def reset_chess_board():
    chess_board = [[3, 4, 5, 6, 7, 5, 4, 3],
                   [2, 2, 2, 2, 2, 2, 2, 2],
                   [1, 1, 1, 1, 1, 1, 1, 1],
                   [1, 1, 1, 1, 1, 1, 1, 1],
                   [1, 1, 1, 1, 1, 1, 1, 1],
                   [1, 1, 1, 1, 1, 1, 1, 1],
                   [8, 8, 8, 8, 8, 8, 8, 8],
                   [9, 10, 11, 12, 13, 11, 10, 9]]
    return chess_board
def randomize_chess_board(curr_chess_board):
    for col in range(0,8):
        for row in range(0,8):
            curr_chess_board[row][col] = randint(2,13)
    return curr_chess_board
def print_chess_board():
    for n in range(0,8):
        print(chess_board[n])
    print("-----------------")
def print_player_turn(player_turn):
    if player_turn == 1:
        print("Player's Turn")
    else:
        print("Opponents Turn")
def in_bounds(row, col):
    return row >= 0 and col >= 0 and row < 8 and col < 8
def check_square_player(piece_value):
    return is_empty_space(piece_value) or is_opponent_piece(piece_value)
def check_square_opponent(piece_value):
    return is_empty_space(piece_value) or is_player_piece(piece_value)
def is_opponent_piece(piece_value):
    return piece_value >= 8
def is_player_piece(piece_value):
    return piece_value < 8 and piece_value > 1
def is_empty_space(piece_value):
    return piece_value == 1

def draw_diagonal_player(curr_chess_board, piece_value, row, col):
    start_row = row
    start_col = col
    #Up-Left
    while row > 0 and col > 0:
        row -= 1
        col -=1
        if is_player_piece(curr_chess_board[row][col]):
            break
        if is_opponent_piece(curr_chess_board[row][col]):
            curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
            break
        curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
    row = start_row
    col = start_col
    #Down-Left
    while row > 0 and col < 7:
        row -= 1
        col +=1
        if is_player_piece(curr_chess_board[row][col]):
            break
        if is_opponent_piece(curr_chess_board[row][col]):
            curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
            break
        curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
    row = start_row
    col = start_col
    #Down-Right
    while row < 7 and col < 7:
        row += 1
        col +=1
        if is_player_piece(curr_chess_board[row][col]):
            break
        if is_opponent_piece(curr_chess_board[row][col]):
            curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
            break
        curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
    row = start_row
    col = start_col
    #Up-Right
    while row < 7 and col > 0:
        row += 1
        col -=1
        if is_player_piece(curr_chess_board[row][col]):
            break
        if is_opponent_piece(curr_chess_board[row][col]):
            curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
            break
        curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
    row = start_row
    col = start_col
    return curr_chess_board
def draw_plus_player(curr_chess_board, piece_value, row, col):
    start_row = row
    start_col = col
    #downwards
    while row < 7:
        row += 1
        if is_player_piece(curr_chess_board[row][col]):
            break
        if is_opponent_piece(curr_chess_board[row][col]):
            curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
            break
        curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
    row = start_row
    #upwards
    while row > 0:
        row -= 1
        if is_player_piece(curr_chess_board[row][col]):
            break
        if is_opponent_piece(curr_chess_board[row][col]):
            curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
            break
        curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
    row = start_row
    #leftwards
    while col > 0:
        col -= 1
        if is_player_piece(curr_chess_board[row][col]):
            break
        if is_opponent_piece(curr_chess_board[row][col]):
            curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
            break
        curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
    col = start_col
    #Rightwards
    while col < 7:
        col += 1
        if is_player_piece(curr_chess_board[row][col]):
            break
        if is_opponent_piece(curr_chess_board[row][col]):
            curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
            break
        curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
    col = start_col
    return curr_chess_board
def draw_pawn_player(curr_chess_board, piece_value, row, col):
    start_row = row
    start_col = col
    attack = 0

    if row == 1:
        row += 1
        if in_bounds(row, col) and is_empty_space(curr_chess_board[row][col]):
            curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
        col -= 1
        if in_bounds(row, col) and is_opponent_piece(curr_chess_board[row][col]):
            curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
        col = start_col
        col += 1
        if in_bounds(row, col) and is_opponent_piece(curr_chess_board[row][col]):
            curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
        col = start_col
        if in_bounds(row, col) and (is_opponent_piece(curr_chess_board[row][col]) or is_player_piece(curr_chess_board[row][col])):
            pass
        else:
            row += 1
            if in_bounds(row, col) and is_empty_space(curr_chess_board[row][col]):
                curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
            row = start_row
    else:
        row += 1
        col += 1
        if in_bounds(row, col) and is_opponent_piece(curr_chess_board[row][col]):
            curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
            attack = 1
        col = start_col
        col -= 1
        if in_bounds(row, col) and is_opponent_piece(curr_chess_board[row][col]):
            curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
            attack = 1
        col = start_col
        if in_bounds(row, col) and is_empty_space(curr_chess_board[row][col]) and not attack:
            curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
    return curr_chess_board
def draw_knight_player(curr_chess_board, piece_value, row, col):
    start_row = row
    start_col = col

    row += 2
    col += 1
    if row < 8 and row >= 0 and col < 8 and col >= 0 and check_square_player(curr_chess_board[row][col]):
        curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
    row = start_row
    col = start_col

    row += 2
    col -= 1
    if row < 8 and row >= 0 and col < 8 and col >= 0 and check_square_player(curr_chess_board[row][col]):
        curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
    row = start_row
    col = start_col

    row += 1
    col += 2
    if row < 8 and row >= 0 and col < 8 and col >= 0 and check_square_player(curr_chess_board[row][col]):
        curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
    row = start_row
    col = start_col

    row += 1
    col += -2
    if row < 8 and row >= 0 and col < 8 and col >= 0 and check_square_player(curr_chess_board[row][col]):
        curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
    row = start_row
    col = start_col

    row -= 1
    col += 2
    if row < 8 and row >= 0 and col < 8 and col >= 0 and check_square_player(curr_chess_board[row][col]):
        curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
    row = start_row
    col = start_col

    row -= 1
    col -= 2
    if row < 8 and row >= 0 and col < 8 and col >= 0 and check_square_player(curr_chess_board[row][col]):
        curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
    row = start_row
    col = start_col

    row -= 2
    col += 1
    if row < 8 and row >= 0 and col < 8 and col >= 0 and check_square_player(curr_chess_board[row][col]):
        curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
    row = start_row
    col = start_col

    row -= 2
    col -= 1
    if row < 8 and row >= 0 and col < 8 and col >= 0 and check_square_player(curr_chess_board[row][col]):
        curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
    row = start_row
    col = start_col

    return curr_chess_board
def draw_king_player(curr_chess_board, piece_value, row, col):
    start_row = row
    start_col = col

    row += 1
    col += 1
    if row < 8 and row >= 0 and col < 8 and col >= 0 and check_square_player(curr_chess_board[row][col]):
        curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
    row = start_row
    col = start_col

    row += 1
    col -= 1
    if row < 8 and row >= 0 and col < 8 and col >= 0 and check_square_player(curr_chess_board[row][col]):
        curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
    row = start_row
    col = start_col

    row += 1
    col += 0
    if row < 8 and row >= 0 and col < 8 and col >= 0 and check_square_player(curr_chess_board[row][col]):
        curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
    row = start_row
    col = start_col

    row += 0
    col += 1
    if row < 8 and row >= 0 and col < 8 and col >= 0 and check_square_player(curr_chess_board[row][col]):
        curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
    row = start_row
    col = start_col

    row += 0
    col -= 1
    if row < 8 and row >= 0 and col < 8 and col >= 0 and check_square_player(curr_chess_board[row][col]):
        curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
    row = start_row
    col = start_col

    row -= 1
    col -= 1
    if row < 8 and row >= 0 and col < 8 and col >= 0 and check_square_player(curr_chess_board[row][col]):
        curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
    row = start_row
    col = start_col

    row -= 1
    col += 0
    if row < 8 and row >= 0 and col < 8 and col >= 0 and check_square_player(curr_chess_board[row][col]):
        curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
    row = start_row
    col = start_col

    row -= 1
    col += 1
    if row < 8 and row >= 0 and col < 8 and col >= 0 and check_square_player(curr_chess_board[row][col]):
        curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
    row = start_row
    col = start_col

    return curr_chess_board
def in_check_player(curr_chess_board):
    curr_chess_board = copy.deepcopy(curr_chess_board)
    in_check = True
    for col in range(0,8):
        for row in range(0,8):
            piece_value = curr_chess_board[row][col]
            if piece_value == Pieces.opponent_pawn.value:
                draw_pawn_opponent(curr_chess_board, piece_value, row, col)
            elif piece_value == Pieces.opponent_rook.value:
                draw_plus_opponent(curr_chess_board, piece_value, row, col)
            elif piece_value == Pieces.opponent_knight.value:
                draw_knight_opponent(curr_chess_board, piece_value, row, col)
            elif piece_value == Pieces.opponent_bishop.value:
                draw_diagonal_opponent(curr_chess_board, piece_value, row, col)
            elif piece_value == Pieces.opponent_queen.value:
                draw_plus_opponent(curr_chess_board, piece_value, row, col)
                draw_diagonal_opponent(curr_chess_board, piece_value, row, col)
            elif piece_value == Pieces.opponent_king.value:
                draw_king_opponent(curr_chess_board, piece_value, row, col)
    for col in range(0,8):
        for row in range(0,8):
            if curr_chess_board[row][col] == Pieces.player_king.value:
                in_check = False
    reset(curr_chess_board)
    return in_check

def draw_diagonal_opponent(curr_chess_board, piece_value, row, col):
    start_row = row
    start_col = col
    #Up-Left
    while row > 0 and col > 0:
        row -= 1
        col -=1
        if is_opponent_piece(curr_chess_board[row][col]):
            break
        if is_player_piece(curr_chess_board[row][col]):
            curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
            break
        curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
    row = start_row
    col = start_col
    #Down-Left
    while row > 0 and col < 7:
        row -= 1
        col +=1
        if is_opponent_piece(curr_chess_board[row][col]):
            break
        if is_player_piece(curr_chess_board[row][col]):
            curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
            break
        curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
    row = start_row
    col = start_col
    #Down-Right
    while row < 7 and col < 7:
        row += 1
        col +=1
        if is_opponent_piece(curr_chess_board[row][col]):
            break
        if is_player_piece(curr_chess_board[row][col]):
            curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
            break
        curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
    row = start_row
    col = start_col
    #Up-Right
    while row < 7 and col > 0:
        row += 1
        col -=1
        if is_opponent_piece(curr_chess_board[row][col]):
            break
        if is_player_piece(curr_chess_board[row][col]):
            curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
            break
        curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
    row = start_row
    col = start_col
    return curr_chess_board
def draw_plus_opponent(curr_chess_board, piece_value, row, col):
    start_row = row
    start_col = col
    #downwards
    while row < 7:
        row += 1
        if is_opponent_piece(curr_chess_board[row][col]):
            break
        if is_player_piece(curr_chess_board[row][col]):
            curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
            break
        curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
    row = start_row
    #upwards
    while row > 0:
        row -= 1
        if is_opponent_piece(curr_chess_board[row][col]):
            break
        if is_player_piece(curr_chess_board[row][col]):
            curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
            break
        curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
    row = start_row
    #leftwards
    while col > 0:
        col -= 1
        if is_opponent_piece(curr_chess_board[row][col]):
            break
        if is_player_piece(curr_chess_board[row][col]):
            curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
            break
        curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
    col = start_col
    #Rightwards
    while col < 7:
        col += 1
        if is_opponent_piece(curr_chess_board[row][col]):
            break
        if is_player_piece(curr_chess_board[row][col]):
            curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
            break
        curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
    col = start_col
    return curr_chess_board
def draw_pawn_opponent(curr_chess_board, piece_value, row, col):
    start_row = row
    start_col = col
    attack = 0

    if row == 6:
        row -= 1
        if in_bounds(row, col) and is_empty_space(curr_chess_board[row][col]):
            curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
        col -= 1
        if in_bounds(row, col) and is_player_piece(curr_chess_board[row][col]):
            curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
        col = start_col
        col += 1
        if in_bounds(row, col) and is_player_piece(curr_chess_board[row][col]):
            curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
        col = start_col
        if in_bounds(row, col) and (is_player_piece(curr_chess_board[row][col]) or is_opponent_piece(curr_chess_board[row][col])):
            pass
        else:
            row -= 1
            if in_bounds(row, col) and is_empty_space(curr_chess_board[row][col]):
                curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
            row = start_row
    else:
        row -= 1
        col += 1
        if in_bounds(row, col) and is_player_piece(curr_chess_board[row][col]):
            curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
            attack = 1
        col = start_col
        col -= 1
        if in_bounds(row, col) and is_player_piece(curr_chess_board[row][col]):
            curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
            attack = 1
        col = start_col
        if in_bounds(row, col) and is_empty_space(curr_chess_board[row][col]) and not attack:
            curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
    return curr_chess_board
def draw_knight_opponent(curr_chess_board, piece_value, row, col):
    start_row = row
    start_col = col

    row += 2
    col += 1
    if row < 8 and row >= 0 and col < 8 and col >= 0 and check_square_opponent(curr_chess_board[row][col]):
        curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
    row = start_row
    col = start_col

    row += 2
    col -= 1
    if row < 8 and row >= 0 and col < 8 and col >= 0 and check_square_opponent(curr_chess_board[row][col]):
        curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
    row = start_row
    col = start_col

    row += 1
    col += 2
    if row < 8 and row >= 0 and col < 8 and col >= 0 and check_square_opponent(curr_chess_board[row][col]):
        curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
    row = start_row
    col = start_col

    row += 1
    col += -2
    if row < 8 and row >= 0 and col < 8 and col >= 0 and check_square_opponent(curr_chess_board[row][col]):
        curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
    row = start_row
    col = start_col

    row -= 1
    col += 2
    if row < 8 and row >= 0 and col < 8 and col >= 0 and check_square_opponent(curr_chess_board[row][col]):
        curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
    row = start_row
    col = start_col

    row -= 1
    col -= 2
    if row < 8 and row >= 0 and col < 8 and col >= 0 and check_square_opponent(curr_chess_board[row][col]):
        curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
    row = start_row
    col = start_col

    row -= 2
    col += 1
    if row < 8 and row >= 0 and col < 8 and col >= 0 and check_square_opponent(curr_chess_board[row][col]):
        curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
    row = start_row
    col = start_col

    row -= 2
    col -= 1
    if row < 8 and row >= 0 and col < 8 and col >= 0 and check_square_opponent(curr_chess_board[row][col]):
        curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
    row = start_row
    col = start_col

    return curr_chess_board
def draw_king_opponent(curr_chess_board, piece_value, row, col):
    start_row = row
    start_col = col

    row += 1
    col += 1
    if row < 8 and row >= 0 and col < 8 and col >= 0 and check_square_opponent(curr_chess_board[row][col]):
        curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
    row = start_row
    col = start_col

    row += 1
    col -= 1
    if row < 8 and row >= 0 and col < 8 and col >= 0 and check_square_opponent(curr_chess_board[row][col]):
        curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
    row = start_row
    col = start_col

    row += 1
    col += 0
    if row < 8 and row >= 0 and col < 8 and col >= 0 and check_square_opponent(curr_chess_board[row][col]):
        curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
    row = start_row
    col = start_col

    row += 0
    col += 1
    if row < 8 and row >= 0 and col < 8 and col >= 0 and check_square_opponent(curr_chess_board[row][col]):
        curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
    row = start_row
    col = start_col

    row += 0
    col -= 1
    if row < 8 and row >= 0 and col < 8 and col >= 0 and check_square_opponent(curr_chess_board[row][col]):
        curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
    row = start_row
    col = start_col

    row -= 1
    col -= 1
    if row < 8 and row >= 0 and col < 8 and col >= 0 and check_square_opponent(curr_chess_board[row][col]):
        curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
    row = start_row
    col = start_col

    row -= 1
    col += 0
    if row < 8 and row >= 0 and col < 8 and col >= 0 and check_square_opponent(curr_chess_board[row][col]):
        curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
    row = start_row
    col = start_col

    row -= 1
    col += 1
    if row < 8 and row >= 0 and col < 8 and col >= 0 and check_square_opponent(curr_chess_board[row][col]):
        curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.make_red)
    row = start_row
    col = start_col

    return curr_chess_board
def in_check_opponent():
    pass

def draw_piece(piece_value, row, col):
    if piece_value < 0:
        screen.blit(red_box, red_box.get_rect(topleft=(col,row)))
        piece_value *= -1
    if piece_value == 2:
        return pawn
    elif piece_value == 3:
        return rook
    elif piece_value == 4:
        return knight
    elif piece_value == 5:
        return bishop
    elif piece_value == 6:
        return queen
    elif piece_value == 7:
        return king
    elif piece_value == 8:
        return opponent_pawn
    elif piece_value == 9:
        return opponent_rook
    elif piece_value == 10:
        return opponent_knight
    elif piece_value == 11:
        return opponent_bishop
    elif piece_value == 12:
        return opponent_queen
    elif piece_value == 13:
        return opponent_king
    else:
        return red_box
def reset(curr_chess_board):
    for col in range(0,8):
        for row in range(0,8):
            curr_chess_board = change_chess_board(curr_chess_board, row, col, Change.reset)
    return  curr_chess_board
def game_over(curr_chess_board):
    player_won_flag = 1
    opponent_won_flag = 1
    for col in range(0,8):
        for row in range(0,8):
            if curr_chess_board[row][col] == 7 or curr_chess_board[row][col] == -7:
                opponent_won_flag = 0
            if curr_chess_board[row][col] == 13 or curr_chess_board[row][col] == -13:
                player_won_flag = 0
    if player_won_flag:
        return 1
    elif opponent_won_flag:
        return -1
    else:
        return 0

def change_chess_board(curr_chess_board, row, col, change):
    if change == Change.reset:
        curr_chess_board[row][col] = abs(curr_chess_board[row][col])
    elif change == Change.make_red:
        curr_chess_board[row][col] *= -1
    elif change == Change.move_piece_from:
        curr_chess_board[row][col] = 1
    return  curr_chess_board
def change_chess_board2(curr_chess_board, row, col, change, piece_value):
    if change == Change.move_piece:
        curr_chess_board[row][col] = piece_value
        #Queen the player Pawn
        if piece_value == 2 and row == 7:
            curr_chess_board[row][col] = 6
        #Queen the opponent pawn
        if piece_value == 8 and row == 0:
            curr_chess_board[row][col] = 12
    return curr_chess_board
def change_turn(player_turn):
    if player_turn:
        player_turn = 0
    else:
        player_turn = 1
    return  player_turn

red_box = pygame.image.load("graphics/Red.png")
red_box = pygame.transform.scale(red_box, (100, 100))

# Pieces
pawn = pygame.image.load("graphics/Pawn.png")
pawn = pygame.transform.scale(pawn, (100, 100))

opponent_pawn = pygame.image.load("graphics/Pawn2.png")
opponent_pawn = pygame.transform.scale(opponent_pawn, (100, 100))

rook = pygame.image.load("graphics/Rook.png")
rook = pygame.transform.scale(rook, (100, 100))

opponent_rook = pygame.image.load("graphics/Rook2.png")
opponent_rook = pygame.transform.scale(opponent_rook, (100, 100))

knight = pygame.image.load("graphics/Knight.png")
knight = pygame.transform.scale(knight, (100, 100))

opponent_knight = pygame.image.load("graphics/Knight2.png")
opponent_knight = pygame.transform.scale(opponent_knight, (100, 100))

bishop = pygame.image.load("graphics/Bishop.png")
bishop = pygame.transform.scale(bishop, (100, 100))

opponent_bishop = pygame.image.load("graphics/Bishop2.png")
opponent_bishop = pygame.transform.scale(opponent_bishop, (100, 100))

queen = pygame.image.load("graphics/Queen.png")
queen = pygame.transform.scale(queen, (100, 100))

opponent_queen = pygame.image.load("graphics/Queen2.png")
opponent_queen = pygame.transform.scale(opponent_queen, (100, 100))

king = pygame.image.load("graphics/King.png")
king = pygame.transform.scale(king, (100, 100))

opponent_king = pygame.image.load("graphics/King2.png")
opponent_king = pygame.transform.scale(opponent_king, (100, 100))
while True:
    # if game_state == Game_State.check:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             pygame.quit()
    #             exit()
    #     print("Here")
    if game_state == Game_State.randomize:
        chess_board = randomize_chess_board(chess_board)
        game_state = Game_State.chess
    if game_state == Game_State.chess:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                #if in_check_player(chess_board) == True:
                 #   game_state = Game_State.check
                  #  continue
                if game_over(chess_board) != 0:
                    chess_board = reset_chess_board()
                    player_win = 0
                    opponent_win = 0
                    player_turn = 1
                    game_state = game_state.main_menu
                print_chess_board()
                print_player_turn(player_turn)
                # print(previous_piece_index)
                col = int(event.pos[0] / 100)
                row = int(event.pos[1] / 100)
                if previous_piece_index == (row,col):
                    # idea for future: stalling. By putting a piece back on its own spot, you can stall the game, not making any moves
                    pass
                elif chess_board[row][col] < 0: #Not the same as clicked on last time, and clicked on a red tile
                    # if in_check_player(chess_board): #Player in check TODO: Fix player turn turnover
                    #     chess_board = change_chess_board2(chess_board, row, col, Change.move_piece, piece_value)
                    #     if in_check_player(chess_board):
                    #         chess_board = change_chess_board2(chess_board, row, col, Change.move_piece, -Pieces.empty_space.value)
                    #         continue
                    #     else:
                    #         chess_board = change_chess_board(chess_board, previous_piece_index[0], previous_piece_index[1], Change.move_piece_from)
                    # else:
                        chess_board = change_chess_board(chess_board, previous_piece_index[0], previous_piece_index[1], Change.move_piece_from)
                        chess_board = change_chess_board2(chess_board, row, col, Change.move_piece, piece_value)
                        if game_over(chess_board) != 0:
                            if game_over(chess_board) == 1:
                                player_win = 1
                            else:
                                opponent_win = 1
                        player_turn = change_turn(player_turn)
                chess_board = reset(chess_board)
                piece_value = chess_board[row][col]
                if player_turn:
                    if is_player_piece(piece_value):
                        chess_board[row][col] *= -1
                        if piece_value == 2:
                            chess_board = draw_pawn_player(chess_board, piece_value, row, col)
                        elif piece_value == 3:
                            chess_board = draw_plus_player(chess_board, piece_value, row, col)
                        elif piece_value == 4:
                            chess_board = draw_knight_player(chess_board, piece_value, row, col)
                        elif piece_value == 5:
                            chess_board = draw_diagonal_player(chess_board, piece_value, row, col)
                        elif piece_value == 6:
                            chess_board = draw_plus_player(chess_board, piece_value, row, col)
                            chess_board = draw_diagonal_player(chess_board, piece_value, row, col)
                        elif piece_value == 7:
                            chess_board = draw_king_player(chess_board, piece_value, row, col)
                else:
                    if is_opponent_piece(piece_value):
                        chess_board[row][col] *= -1
                        if piece_value == Pieces.opponent_pawn.value:
                            chess_board = draw_pawn_opponent(chess_board, piece_value, row, col)
                        elif piece_value == Pieces.opponent_rook.value:
                            chess_board = draw_plus_opponent(chess_board, piece_value, row, col)
                        elif piece_value == Pieces.opponent_knight.value:
                            chess_board = draw_knight_opponent(chess_board, piece_value, row, col)
                        elif piece_value == Pieces.opponent_bishop.value:
                            chess_board = draw_diagonal_opponent(chess_board, piece_value, row, col)
                        elif piece_value == Pieces.opponent_queen.value:
                            chess_board = draw_plus_opponent(chess_board, piece_value, row, col)
                            chess_board = draw_diagonal_opponent(chess_board, piece_value, row, col)
                        elif piece_value == Pieces.opponent_king.value:
                            chess_board = draw_king_opponent(chess_board, piece_value, row, col)

                previous_piece_index = (row, col)
                # print("Column: ",col, "Row: ", row)

        if player_win == 0 and opponent_win == 0:
            screen.blit(board_surface, board_rect)
            for col in range(0,8):
                for row in range(0,8):
                    if chess_board[row][col] != 1:
                        screen.blit(draw_piece(chess_board[row][col],row*100,col*100), red_box.get_rect(topleft=(col*100,row*100)))
        else:
            screen.blit(pygame.image.load("graphics/Black.png"), red_box.get_rect(topleft=(0, 0)))
            if player_win:
                screen.blit(pygame.image.load("graphics/Win.png"), red_box.get_rect(topleft=(0,0)))
            if opponent_win:
                screen.blit(pygame.image.load("graphics/Lose.png"), red_box.get_rect(topleft=(0, 0)))
    elif game_state == Game_State.main_menu:
        background_surface = pygame.image.load("graphics/Main Menu Background.png")
        chess2_surface = pygame.image.load("graphics/Chess2.png")
        play_button_surface = pygame.image.load("graphics/Play Button.png")
        play_button_rect = play_button_surface.get_rect(bottomleft=(10,790))
        random_play_button_surface = pygame.image.load("graphics/Play Button.png")
        random_play_button_rect = random_play_button_surface.get_rect(bottomright=(790, 790))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    game_state = Game_State.chess
                if random_play_button_rect.collidepoint(event.pos):
                    game_state = Game_State.randomize
        screen.blit(background_surface, (0,0))
        screen.blit(chess2_surface, (0, 0))
        screen.blit(play_button_surface, play_button_rect)
        screen.blit(random_play_button_surface, random_play_button_rect)

    pygame.display.update()
    clock.tick(60)
