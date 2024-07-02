import pygame
import sys
import socket
import threading
import json
from entities import Paddle, Ball
from enum import Enum

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Constants
WIDTH = 900
HEIGHT = 500
EROTIC_RED = pygame.Color(35, 27, 255) # BGR
WHITE = pygame.Color(255, 255, 255)
BLACK = pygame.Color(0, 0, 0)

SPEED_INCREMENT = 1.05

score1, score2 = 0, 0

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dong Erotica")

# Initialize font
pygame.font.init()
font = pygame.font.Font(None, 74)

# Create paddle and ball globally
paddle1 = Paddle(30, HEIGHT // 2 - 60, 10, 120)
paddle2 = Paddle(WIDTH - 40, HEIGHT // 2 - 60, 10, 120)
ball = Ball(WIDTH // 2, HEIGHT // 2, 15)
game_over = False

# Load music
pygame.mixer.music.load('soundtrack1.mp3')
pygame.mixer.music.play(-1)

# Load hit sound effects
paddle_hit_sound = pygame.mixer.Sound('sound-effect.mp3')
wall_hit_sound = pygame.mixer.Sound('sound-effect3.mp3')

# Load background images
home_screen = pygame.image.load('background-e.jpg')
home_screen = pygame.transform.scale(home_screen, (WIDTH, HEIGHT))

background_image = pygame.image.load('pong-background.png')
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

waiting_image = pygame.image.load('joe-byron.jpg')
waiting_image = pygame.transform.scale(waiting_image, (WIDTH, HEIGHT))

game_over_image = pygame.image.load('end-game-pic.jpg')
game_over_image = pygame.transform.scale(game_over_image, (WIDTH, HEIGHT))

# Define game states
class GameState(Enum):
    MAIN_MENU = 1
    SPLIT_SCREEN = 2
    ONLINE = 3
    GAME_OVER = 4

# Define online game states
class OnlineState(Enum):
    WAITING = 1
    IN_GAME = 2
    GAME_OVER = 3

# Initialize game state
game_state = GameState.MAIN_MENU

# Initialize online state
online_state = OnlineState.WAITING

# Network setup
HOST = "127.0.1.0"  # Corrected IP address for local testing
PORT = 12345
client_socket = None
client_role = None

def connect_to_server():
    global client_socket
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PORT))
        thread = threading.Thread(target=receive_data)
        thread.start()
    except socket.error as se:
        print(f"Socket error: {se}")

def receive_data():
    global paddle1, paddle2, ball, score1, score2, online_state, client_role
    decoder = json.JSONDecoder()
    buffer = ""
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if data:
                buffer += data
                while buffer:
                    try:
                        game_data, idx = decoder.raw_decode(buffer)
                        buffer = buffer[idx:].lstrip()
                        if 'role' in game_data:
                            client_role = game_data['role']
                            print(f"Assigned role: {client_role}")
                        elif game_data.get('type') == 'start_game':
                            online_state = OnlineState.IN_GAME
                        elif game_data.get('game_over') == True:
                            online_state = OnlineState.GAME_OVER
                        else:
                            update_game_state(game_data)
                    except ValueError:
                        # Incomplete JSON object received, wait for more data
                        break
        except socket.error as se:
            print(f"Socket error: {se}")
            break
        except Exception as e:
            print(f"Error receiving data: {e}")
            break

def update_game_state(game_data):
    global paddle1, paddle2, ball, score1, score2
    if 'paddle1_y' in game_data:
        paddle1.rect.y = game_data['paddle1_y']
    if 'paddle2_y' in game_data:
        paddle2.rect.y = game_data['paddle2_y']
    if 'ball_x' in game_data:
        ball.rect.x = game_data['ball_x']
    if 'ball_y' in game_data:
        ball.rect.y = game_data['ball_y']
    if 'score1' in game_data:
        score1 = game_data['score1']
    if 'score2' in game_data:
        score2 = game_data['score2']

def send_data():
    game_data = {
        'paddle1_y': paddle1.rect.y,
        'paddle2_y': paddle2.rect.y,
        'ball_x': ball.rect.x,
        'ball_y': ball.rect.y,
        'score1': score1,
        'score2': score2
    }
    try:
        message = json.dumps(game_data) + '\n'
        client_socket.sendall(message.encode())
    except ConnectionError as e:
        print(f"Connection Error: {e}")
    except Exception as e:
        print(f"Error sending data: {e}")

# Main Loop
def main():
    global score1, score2
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if game_state == GameState.MAIN_MENU:
            handle_main_menu()
        elif game_state == GameState.SPLIT_SCREEN:
            handle_split_screen(paddle1, paddle2, ball, clock)
        elif game_state == GameState.ONLINE:
            handle_online()
        elif game_state == GameState.GAME_OVER:
            draw_game_over()

        pygame.display.flip()
        clock.tick(60)

# Main Menu
def handle_main_menu():
    global game_state
    screen.blit(home_screen, (0, 0))

    # Menu text
    menu_text = font.render("Main Menu", True, EROTIC_RED)
    screen.blit(menu_text, (WIDTH // 2 - menu_text.get_width() // 2, HEIGHT // 4 - menu_text.get_height() // 4))

    # Split screen text
    split_screen_text = font.render("1: Split Screen", True, EROTIC_RED)
    screen.blit(split_screen_text, (WIDTH // 4 - split_screen_text.get_width() // 1.5 + 100, HEIGHT // 2 - split_screen_text.get_height() // 2))

    # Online text
    online_text = font.render("2: Online", True, EROTIC_RED)
    screen.blit(online_text, (WIDTH // 2 + 100, HEIGHT // 2 - online_text.get_height() // 2))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_1]:
        game_state = GameState.SPLIT_SCREEN
    if keys[pygame.K_2]:
        game_state = GameState.ONLINE
        connect_to_server()

# Split screen
def handle_split_screen(paddle1, paddle2, ball, clock):
    global score1, score2, game_state, game_over

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # check if game is over
    if score1 == 2 or score2 == 2:
        game_over = True
        game_state = GameState.GAME_OVER

    # Check for user input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and paddle1.rect.top > 0:
        paddle1.move(up=True)
    if keys[pygame.K_s] and paddle1.rect.bottom < HEIGHT:
        paddle1.move(up=False)
    if keys[pygame.K_UP] and paddle2.rect.top > 0:
        paddle2.move(up=True)
    if keys[pygame.K_DOWN] and paddle2.rect.bottom < HEIGHT:
        paddle2.move(up=False)
    if keys[pygame.K_ESCAPE]:
        game_state = GameState.MAIN_MENU

    ball.move()

    # Check for top to bottom ball collision
    if ball.rect.top <= 0 or ball.rect.bottom >= HEIGHT:
        ball.speed_y *= -1
        ball.speed_x *= SPEED_INCREMENT
        ball.speed_y *= SPEED_INCREMENT
        wall_hit_sound.play()

    # Check for player to ball collision
    if ball.rect.colliderect(paddle1.rect) or ball.rect.colliderect(paddle2.rect):
        ball.speed_x *= -1
        ball.speed_x *= SPEED_INCREMENT
        ball.speed_y *= SPEED_INCREMENT
        paddle_hit_sound.play()

    # Check if paddle2 scores
    if ball.rect.left <= 0:
        score2 += 1
        ball.reset(WIDTH // 2, HEIGHT // 2)
        ball.speed_x = 4
        ball.speed_y = 4

    # Check if paddle1 scores
    if ball.rect.right >= WIDTH:
        score1 += 1
        ball.reset(WIDTH // 2, HEIGHT // 2)
        ball.speed_x = 4
        ball.speed_y = 4

    # Draw screen
    screen.blit(background_image, (0, 0))

    # Draw paddles
    paddle1.draw(screen)
    paddle2.draw(screen)

    # Draw ball
    ball.draw(screen)

    # Draw score
    score_text = font.render(f"{score1} - {score2}", True, EROTIC_RED)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 10))


def handle_waiting():
    screen.blit(waiting_image, (0, 0))
    waiting_text = font.render("Waiting for player...", True, EROTIC_RED)
    screen.blit(waiting_text, (WIDTH // 2 - waiting_text.get_width() // 2, HEIGHT // 2))


def handle_in_game():
    global client_role, paddle1, paddle2

    keys = pygame.key.get_pressed()
    if client_role == 'Player 1':
        # Check for user input
        if keys[pygame.K_w] and paddle1.rect.top > 0:
            paddle1.move(up=True)
            send_paddle_position()
        elif keys[pygame.K_s] and paddle1.rect.bottom < HEIGHT:
            paddle1.move(up=False)
            send_paddle_position()
    elif client_role == 'Player 2':
        if keys[pygame.K_w] and paddle2.rect.top > 0:
            paddle2.move(up=True)
            send_paddle_position()
        elif keys[pygame.K_s] and paddle2.rect.bottom < HEIGHT:
            paddle2.move(up=False)
            send_paddle_position()

    # Draw screen
    screen.blit(background_image, (0, 0))

    # Draw paddles
    paddle1.draw(screen)
    paddle2.draw(screen)

    # Draw ball
    ball.draw(screen)

    # Draw score
    score_text = font.render(f"{score1} - {score2}", True, EROTIC_RED)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 10))



def send_paddle_position():
    game_data = {
        'paddle1_y': paddle1.rect.y,
        'paddle2_y': paddle2.rect.y,
        'type': 'update'
    }
    try:
        message = json.dumps(game_data) + '\n'
        client_socket.sendall(message.encode())
    except ConnectionError as e:
        print(message)
        print(f"Connection error: {e}")
    except Exception as e:
        print(f"Error sending data: {e}")



def draw_game_over():
    screen.blit(game_over_image, (0, 0))

    # Menu text
    menu_text = font.render("Game Over", True, EROTIC_RED)
    screen.blit(menu_text, (WIDTH // 2 - menu_text.get_width() // 2, HEIGHT // 4 - menu_text.get_height() // 4))

# Online
def handle_online():
    global game_state, online_state

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if online_state == OnlineState.WAITING:
        handle_waiting()
    elif online_state == OnlineState.IN_GAME:
        handle_in_game()
    elif online_state == OnlineState.GAME_OVER:
        draw_game_over()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        game_state = GameState.MAIN_MENU

if __name__ == "__main__":
    main()
