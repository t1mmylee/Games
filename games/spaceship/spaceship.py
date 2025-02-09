import pygame
import os
import time

pygame.font.init()
pygame.mixer.init()

# Constants
WIDTH, HEIGHT = 1200, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Raid")

# Colors
WHITE = (255, 255, 255)
GRAY = (194, 197, 204)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
B_BLUE = (137, 207, 240)

# Game Variables
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)
HEALTH_FONT = pygame.font.SysFont('comicsans', 25)
WINNER_FONT = pygame.font.SysFont('Verdana', 80)
MENU_FONT = pygame.font.SysFont('comicsans', 50)
CONTACT_FONT = pygame.font.SysFont('comicsans', 30)
HELP_FONT = pygame.font.SysFont('comicsans', 20)

FPS = 100
VEL = 2.7
BULLET_VEL = 7
MAX_BULLETS = 6
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

# Events
YELLOW_HIT = pygame.USEREVENT + 0
RED_HIT = pygame.USEREVENT + 1

# Load Images
YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('(loaction of asset->)\\spaceship\\Assets\\spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('(loaction of asset->)\\spaceship\\Assets\\spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('(loaction of asset->)\\spaceship\\Assets\\space.png')), (WIDTH, HEIGHT))

# Cooldown Variables
YELLOW_COOLDOWN = 0
RED_COOLDOWN = 0

# Draw Window Function
def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()

# Handle Movement Function
def handle_movement(keys_pressed, player, left_bound, right_bound, up_bound, down_bound):
    if keys_pressed[left_bound] and player.x - VEL > 0:
        player.x -= VEL
    if keys_pressed[right_bound] and player.x + VEL + player.width < WIDTH:
        player.x += VEL
    if keys_pressed[up_bound] and player.y - VEL > 0:
        player.y -= VEL
    if keys_pressed[down_bound] and player.y + VEL + player.height < HEIGHT:
        player.y += VEL

# Handle Bullets Function
def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

# Draw Winner Function
def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() / 2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

#Menu Screen
def menu_screen():
    run = True
    while run:
        WIN.fill(GRAY)
        title = MENU_FONT.render("Welcome to the Space Raid", 1, BLACK)
        WIN.blit(title, (WIDTH / 2 - title.get_width() / 2, 100))

        # Updated button dimensions
        button_width, button_height = 300, 80
        play_button = pygame.Rect(WIDTH / 2 - button_width / 2, 250, button_width, button_height)
        contact_button = pygame.Rect(WIDTH / 2 - button_width / 2, 370, button_width, button_height)
        help_button = pygame.Rect(WIDTH / 2 - button_width / 2, 490, button_width, button_height)

        # Draw buttons with rounded edges
        pygame.draw.rect(WIN, WHITE, play_button, border_radius=20)
        pygame.draw.rect(WIN, WHITE, contact_button, border_radius=20)
        pygame.draw.rect(WIN, WHITE, help_button, border_radius=20)

        # Render and center text
        play_text = MENU_FONT.render("Play", 1, B_BLUE)
        contact_text = MENU_FONT.render("Contact", 1, B_BLUE)
        help_text = MENU_FONT.render("Help", 1, B_BLUE)

        WIN.blit(play_text, (play_button.centerx - play_text.get_width() / 2, play_button.centery - play_text.get_height() / 2))
        WIN.blit(contact_text, (contact_button.centerx - contact_text.get_width() / 2, contact_button.centery - contact_text.get_height() / 2))
        WIN.blit(help_text, (help_button.centerx - help_text.get_width() / 2, help_button.centery - help_text.get_height() / 2))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if play_button.collidepoint(mouse_pos):
                    main()
                if contact_button.collidepoint(mouse_pos):
                    contact_screen()
                if help_button.collidepoint(mouse_pos):
                    help_screen()


# Contact Screen Function
def contact_screen():
    run = True
    while run:
        WIN.fill(BLACK)
        title = MENU_FONT.render("Contact", 1, WHITE)
        WIN.blit(title, (WIDTH/2 - title.get_width()/2, 100))

        email_text = CONTACT_FONT.render("Email: carlohallaltarraf@gmail.com", 1, WHITE)
        WIN.blit(email_text, (WIDTH/2 - email_text.get_width()/2, 300))

        back_button = pygame.Rect(WIDTH/2 - 100, 450, 200, 50)
        pygame.draw.rect(WIN, BLUE, back_button)
        back_text = MENU_FONT.render("Back", 1, WHITE)
        WIN.blit(back_text, (WIDTH/2 - back_text.get_width()/2, 460))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if back_button.collidepoint(mouse_pos):
                    menu_screen()

# Help Screen Function
def help_screen():
    run = True
    while run:
        WIN.fill(BLACK)
        title = MENU_FONT.render("Help", 1, WHITE)
        WIN.blit(title, (WIDTH/2 - title.get_width()/2, 100))

        help_text1 = HELP_FONT.render("This is a 2-player spaceship game.", 1, WHITE)
        help_text2 = HELP_FONT.render("Player 1 (Yellow) controls: W, A, S, D, LCTRL to shoot.", 1, WHITE)
        help_text3 = HELP_FONT.render("Player 2 (Red) controls: UP, DOWN, LEFT, RIGHT, RCTRL to shoot.", 1, WHITE)
        help_text4 = HELP_FONT.render("The goal is to reduce the opponent's health to zero.", 1, WHITE)

        WIN.blit(help_text1, (WIDTH/2 - help_text1.get_width()/2, 200))
        WIN.blit(help_text2, (WIDTH/2 - help_text2.get_width()/2, 250))
        WIN.blit(help_text3, (WIDTH/2 - help_text3.get_width()/2, 300))
        WIN.blit(help_text4, (WIDTH/2 - help_text4.get_width()/2, 350))

        back_button = pygame.Rect(WIDTH/2 - 100, 450, 200, 50)
        pygame.draw.rect(WIN, BLUE, back_button)
        back_text = MENU_FONT.render("Back", 1, WHITE)
        WIN.blit(back_text, (WIDTH/2 - back_text.get_width()/2, 460))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if back_button.collidepoint(mouse_pos):
                    menu_screen()

# Main Function
def main():
    global YELLOW_COOLDOWN, RED_COOLDOWN

    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_health = 25
    yellow_health = 25

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                # Yellow spaceship shooting
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS and YELLOW_COOLDOWN == 0:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    if len(yellow_bullets) >= 9:
                        YELLOW_COOLDOWN = time.time()

                # Red spaceship shooting
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS and RED_COOLDOWN == 0:
                    bullet = pygame.Rect(
                        red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    if len(red_bullets) >= 9:
                        RED_COOLDOWN = time.time()

            if event.type == RED_HIT:
                red_health -= 1

            if event.type == YELLOW_HIT:
                yellow_health -= 1

        # Cooldown handling
        if YELLOW_COOLDOWN > 0:
            if time.time() - YELLOW_COOLDOWN >= 4:
                YELLOW_COOLDOWN = 0
        if RED_COOLDOWN > 0:
            if time.time() - RED_COOLDOWN >= 4:
                RED_COOLDOWN = 0

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"
        if yellow_health <= 0:
            winner_text = "Red Wins!"
        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        handle_movement(keys_pressed, yellow, pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s)
        handle_movement(keys_pressed, red, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

    menu_screen()

if __name__ == "__main__":
    menu_screen()
