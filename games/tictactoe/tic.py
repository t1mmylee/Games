import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 900, 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TicTacToe")
BG_COLOR = (194, 197, 204)
GRAY = (194, 197, 204)

FONT = pygame.font.Font("C:\\Users\\carlo\\OneDrive\\Desktop\\Carlo Games\\tictactoe\\assets\\Roboto-Regular.ttf", 100)
BUTTON_FONT = pygame.font.Font("C:\\Users\\carlo\\OneDrive\\Desktop\\Carlo Games\\tictactoe\\assets\\Roboto-Regular.ttf", 60)  # Bold font

BOARD = pygame.image.load("C:\\Users\\carlo\\OneDrive\\Desktop\\Carlo Games\\tictactoe\\assets\\Board.png")
X_IMG = pygame.image.load("C:\\Users\\carlo\\OneDrive\\Desktop\\Carlo Games\\tictactoe\\assets\\X.png")
O_IMG = pygame.image.load("C:\\Users\\carlo\\OneDrive\\Desktop\\Carlo Games\\tictactoe\\assets\\O.png")

board = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
graphical_board = [[[None, None], [None, None], [None, None]],
                   [[None, None], [None, None], [None, None]],
                   [[None, None], [None, None], [None, None]]]

to_move = "X"

SCREEN.fill(BG_COLOR)
SCREEN.blit(BOARD, (64, 64))

pygame.display.update()

def render_board(board, ximg, oimg):
    global graphical_board
    for i in range(3):
        for j in range(3):
            if board[i][j] == 'X':
                graphical_board[i][j][0] = ximg
                graphical_board[i][j][1] = ximg.get_rect(center=(j * 300 + 150, i * 300 + 150))

            elif board[i][j] == 'O':
                graphical_board[i][j][0] = oimg
                graphical_board[i][j][1] = oimg.get_rect(center=(j * 300 + 150, i * 300 + 150))

def add_XO(board, graphical_board, to_move):
    current_pos = pygame.mouse.get_pos()
    converted_x = (current_pos[0] - 64) // 300
    converted_y = (current_pos[1] - 64) // 300
    if 0 <= converted_x < 3 and 0 <= converted_y < 3:
        if board[converted_y][converted_x] not in ['X', 'O']:
            board[converted_y][converted_x] = to_move
            to_move = 'O' if to_move == 'X' else 'X'

    render_board(board, X_IMG, O_IMG)

    for i in range(3):
        for j in range(3):
            if graphical_board[i][j][0] is not None:
                SCREEN.blit(graphical_board[i][j][0], graphical_board[i][j][1])
    
    return board, to_move

game_finished = False
winner = None

def check_win(board):
    global winner
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] and board[row][0] is not None:
            winner = board[row][0]
            for i in range(3):
                graphical_board[row][i][0] = pygame.image.load(f"C:\\Users\\carlo\\OneDrive\\Desktop\\Carlo Games\\tictactoe\\assets\\Winning {winner}.png")
                SCREEN.blit(graphical_board[row][i][0], graphical_board[row][i][1])
            pygame.display.update()
            return winner

    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not None:
            winner = board[0][col]
            for i in range(3):
                graphical_board[i][col][0] = pygame.image.load(f"C:\\Users\\carlo\\OneDrive\\Desktop\\Carlo Games\\tictactoe\\assets\\Winning {winner}.png")
                SCREEN.blit(graphical_board[i][col][0], graphical_board[i][col][1])
            pygame.display.update()
            return winner
   
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        winner = board[0][0]
        for i in range(3):
            graphical_board[i][i][0] = pygame.image.load(f"C:\\Users\\carlo\\OneDrive\\Desktop\\tictactoe\\assets\\Winning {winner}.png")
            SCREEN.blit(graphical_board[i][i][0], graphical_board[i][i][1])
        pygame.display.update()
        return winner
          
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        winner = board[0][2]
        for i in range(3):
            graphical_board[i][2 - i][0] = pygame.image.load(f"C:\\Users\\carlo\\OneDrive\\Desktop\\Carlo Games\\tictactoe\\assets\\Winning {winner}.png")
            SCREEN.blit(graphical_board[i][2 - i][0], graphical_board[i][2 - i][1])
        pygame.display.update()
        return winner
    
    if winner is None:
        for i in range(3):
            for j in range(3):
                if board[i][j] not in ['X', 'O']:
                    return None
        return "DRAW"

def draw_rounded_button(surface, color, rect, radius=20):
    """Draw a rounded rectangle button."""
    pygame.draw.rect(surface, color, rect, border_radius=radius)

def draw_winner_screen(winner):
    global game_finished

    # Darken the screen
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 190))  # Semi-transparent black
    SCREEN.blit(overlay, (0, 0))

    # Display winner message
    if winner == "DRAW":
        winner_text = FONT.render("It's a Draw!", True, (255, 255, 255))
    else:
        winner_text = FONT.render(f"Player {winner} Wins!", True, (255, 255, 255))
    SCREEN.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2 - winner_text.get_height() // 2 - 100))

    # Play Again button
    play_again_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 20, 300, 80)  # Bigger button
    draw_rounded_button(SCREEN, (200, 200, 200), play_again_button, radius=20)  # Light grey rounded button

    # Center the "Play Again" text in the button
    play_again_text = BUTTON_FONT.render("Play Again", True, (50, 50, 50))  # Dark grey bold text
    text_rect = play_again_text.get_rect(center=play_again_button.center)  # Center text in the button
    SCREEN.blit(play_again_text, text_rect)

    pygame.display.update()

    return play_again_button

def reset_game():
    global board, graphical_board, to_move, game_finished, winner
    board = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    graphical_board = [[[None, None], [None, None], [None, None]],
                       [[None, None], [None, None], [None, None]],
                       [[None, None], [None, None], [None, None]]]
    to_move = "X"
    game_finished = False
    winner = None
    SCREEN.fill(BG_COLOR)
    SCREEN.blit(BOARD, (64, 64))
    pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and not game_finished:
            board, to_move = add_XO(board, graphical_board, to_move)

            if check_win(board) is not None:
                game_finished = True
                play_again_button = draw_winner_screen(winner)

        if game_finished and event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if play_again_button.collidepoint(mouse_pos):
                reset_game()

    pygame.display.update()