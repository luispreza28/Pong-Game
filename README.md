# Pong Game with Online Multiplayer
## Overview
This project is a modernized version of the classic Pong game implemented using Python and Pygame. It supports both local split-screen play and online multiplayer mode. The game features a dynamic user interface with multiple game states, sound effects, and background music.

The online multiplayer mode allows two players to connect via sockets, take on the roles of either Player 1 or Player 2, and play against each other remotely. The game logic ensures smooth gameplay with ball movement, paddle collisions, scoring, and win conditions.

## Features
- Local Split-Screen Mode: Play with a friend on the same machine.

- Online Multiplayer Mode: Connect two players over a network using a client-server architecture.

- Dynamic Background and Sounds: Enjoy background music and sound effects for paddle hits and wall collisions.

- Main Menu: Easily switch between local and online modes.

- Game Over Screen: Display the winner after one player scores a predetermined number of points.

- Game Reset: Restart the game with paddles, ball positions, and scores reset to their initial state.

## Requirements

- Python 3.x

- Pygame library

- A stable internet connection (for online multiplayer mode)

## Installation
### Clone the Repository:

```git clone https://github.com/your-username/pong-game-multiplayer.git```
```cd pong-game-multiplayer```

### Install Dependencies 
- Ensure that you have Python installed, then install the required libraries.

```pip install pygame```

### Set Up Game Files: Ensure that the following assets are in the project folder:

- soundtrack1.mp3
- osu-sound-hit.mp3
- wall-hit-sound.mp3
- home-screen-image.jpeg
- pong-background.png
- joe-byron.jpg
- kitty-end-game-image.jpg
### These files are essential for background images, sound effects, and music.

## Usage
### 1. Running the Game in Local Split-Screen Mode
To play locally on the same machine:

```python client.py```

- Select the "1: Split Screen" option in the main menu.

### 2. Running the Game in Online Multiplayer Mode
Step 1: Start the Server

```python server.py```
The server will start listening for incoming connections.

### Step 2: Connect Clients
Run the client.py on two separate machines (or two terminal instances for local testing) and select the "2: Online" option in the main menu.

## File Structure


pong-game-multiplayer/

│

├── client.py                  # Main game client (includes local and online multiplayer)

├── server.py                  # Server script for handling multiplayer

├── entities.py                # Paddle and Ball class definitions

├── README.md                  # Documentation file

├── home-screen-image.jpeg      # Main menu background image

├── pong-background.png         # Game background image

├── joe-byron.jpg               # Waiting screen image for online mode

├── kitty-end-game-image.jpg    # Game over screen image

├── soundtrack1.mp3             # Background music

├── osu-sound-hit.mp3           # Paddle hit sound effect

└── wall-hit-sound.mp3          # Wall hit sound effect

## Game Modes
### Local Split-Screen Mode
In this mode, both players use the same keyboard to control their paddles. Player 1 uses W and S to move their paddle, while Player 2 uses the arrow keys. The game ends when one player scores 2 points.

### Online Multiplayer Mode
In this mode, two players connect over a network. The server assigns each player as Player 1 or Player 2. Once both players are connected, the game begins. Players use the same keys as in split-screen mode to control their paddles. The first player to score 1 point wins.

- Waiting for Connection: If only one player connects to the server, they will see a waiting screen until the second player joins.
- End of Game: The game ends when one player scores the winning point, and the client displays a game-over screen with a countdown to return to the main menu.
  
## Controls
### Local Split-Screen Mode
#### Player 1:
- Move Up: W
- Move Down: S
#### Player 2:
- Move Up: Up Arrow
- Move Down: Down Arrow
### Online Multiplayer Mode
#### Player 1:
- Move Up: W
- Move Down: S
#### Player 2:
- Move Up: W
- Move Down: S
#### Common Controls
- Escape Key: Return to the main menu.

## Network Setup
To run the online multiplayer mode, you must configure the network properly:

#### Server Setup:

- The server.py file should be run on the server machine (or localhost for local testing).

#### Client Setup:

- In client.py, ensure that the HOST variable is set to the IP address of the server machine. Both clients will connect to this IP address to play.
 
- Port: The default port is set to 12345. Ensure this port is open and not blocked by firewalls.

## Known Issues
- Socket Disconnections: If a client disconnects during an online game, the server will not handle reconnections during the same session. A full game restart is required.
  
- Client-Server Latency: Depending on the network conditions, slight delays might be experienced between clients, especially if the server is running on a remote machine.
  
## Contributors
- Luis Preza – Developer
- Pygame Community – Inspiration and resources
