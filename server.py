import socket
import threading
import json
from entities import Ball, Paddle
import time

# Server constants
HOST = "127.0.1.0"  # Adjusted the host address
PORT = 12345

lock = threading.Lock()
clients = []
connected_clients = 0
game_state = "WAITING"
roles = ["Player 1", "Player 2"]

WIDTH = 900
HEIGHT = 500
paddle1 = Paddle(30, HEIGHT // 2 - 60, 10, 120)
paddle2 = Paddle(WIDTH - 40, HEIGHT // 2 - 60, 10, 120)
ball = Ball(WIDTH // 2, HEIGHT // 2, 15)
score1, score2 = 0, 0
winner = None
game_over = False


# Handle Client
def handle_client(client_socket):
    global connected_clients, game_state, clients, ball, paddle1, paddle2, score1, score2

    # Check to ensure the number of clients does not exceed available roles
    with lock:
        client_role = roles[len(clients) % len(roles)]  # Use modulo to cycle through roles
        connected_clients += 1
        clients.append(client_socket)

    if connected_clients == 2:
        with lock:
            game_state = 'IN_GAME'
            start_game()

    try:
        client_socket.sendall(json.dumps({'role': client_role}).encode())
        buffer = ""
        while True:
            data = client_socket.recv(2048).decode()
            if data:
                buffer += data
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    try:
                        game_data = json.loads(line)
                        update_game_state(game_data)
                        broadcast(game_data, client_socket)
                    except json.JSONDecodeError as je:
                        print(f"Error decoding JSON: {je}")
    except socket.error as se:
        print(f"Socket error: {se}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        with lock:
            connected_clients -= 1
            clients.remove(client_socket)
            if connected_clients < 2:
                game_state = 'WAITING'
        client_socket.close()


def update_game_state(game_data):
    global paddle1, paddle2
    if 'paddle1_y' in game_data:
        paddle1.rect.y = game_data['paddle1_y']
    if 'paddle2_y' in game_data:
        paddle2.rect.y = game_data['paddle2_y']


def start_game():
    state = {
        'paddle1_y': paddle1.rect.y,
        'paddle2_y': paddle2.rect.y,
        'ball_x': ball.rect.x,
        'ball_y': ball.rect.y,
        'score1': score1,
        'score2': score2,
        'type': 'start_game',
        'winner': winner,
        'game_state': game_state
    }
    for client in clients:
        client.sendall(json.dumps(state).encode())


def broadcast(game_data, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                game_data['game_state'] = game_state
                client.sendall((json.dumps(game_data) + '\n').encode())
            except BrokenPipeError:
                print(f"Client {client} has disconnected.")
                clients.remove(client)  # Remove the disconnected client


def game_loop():
    global ball, paddle1, paddle2, score1, score2, game_over, winner, connected_clients, game_state
    while True:
        with lock:
            if connected_clients < 2:
                state = {'waiting': True}
                broadcast(state, None)

            elif connected_clients == 1:
                game_state = 'IN_GAME'

            if game_state == 'IN_GAME':
                ball.move()
                # Check for top and bottom collision
                if ball.rect.top <= 0 or ball.rect.bottom >= HEIGHT:
                    ball.speed_y *= -1

                # Check for paddle collision
                if ball.rect.colliderect(paddle1.rect) or ball.rect.colliderect(paddle2.rect):
                    ball.speed_x *= -1

                # Check for scoring
                if ball.rect.left <= 0:
                    score2 += 1
                    ball.reset(WIDTH // 2, HEIGHT // 2)
                elif ball.rect.right >= WIDTH:
                    score1 += 1
                    ball.reset(WIDTH // 2, HEIGHT // 2)

                # check if score is 5
                if score1 == 1 or score2 ==1:
                    game_over = True
                    winner = roles[0] if score1 == 1 else roles[1]

                # Broadcast the updated state
                state = {
                    'paddle1_y': paddle1.rect.y,
                    'paddle2_y': paddle2.rect.y,
                    'ball_x': ball.rect.x,
                    'ball_y': ball.rect.y,
                    'score1': score1,
                    'score2': score2,
                    'type': 'update',
                    'game_over': game_over,
                    'winner': winner,
                }
                broadcast(state, None)

                print(f"Number of connected clients {connected_clients}")
                # Wait for a few seconds before resetting the game
                if game_over:
                    state = {
                        'type': 'game_over',
                        'winner': winner,
                        'game_state': game_state,
                        'score1': score1,
                        'score2': score2
                    }
                    broadcast(state, None)
                    time.sleep(5)
                    reset_game()

        time.sleep(1/60)


# Define function for starting server
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(2)
    print(f"Server started on {HOST}:{PORT}")

    game_thread = threading.Thread(target=game_loop)
    game_thread.start()

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn,))
        thread.start()


# Reset game function
def reset_game():
    global ball, paddle1, paddle2, score1, score2, game_over, game_state, connected_clients, clients
    paddle1 = Paddle(30, HEIGHT // 2 - 60, 10, 120)
    paddle2 = Paddle(WIDTH - 40, HEIGHT // 2 - 60, 10, 120)
    ball = Ball(WIDTH // 2, HEIGHT // 2, 15)
    score1, score2 = 0, 0
    game_over = False
    game_state = 'WAITING'  # Ensure the game state is reset
    clients.clear()         # Ensure clients list is cleared
    connected_clients = 0   # Reset the connected clients count



if __name__ == "__main__":
    start_server()
