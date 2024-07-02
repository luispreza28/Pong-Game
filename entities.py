import pygame

WHITE = (255,255,255)


# Paddle Class
class Paddle:

    # Constructor
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = 5

    # Move function
    def move(self, up=True):
        if up:
            self.rect.y -= self.speed
        else:
            self.rect.y += self.speed

    # Draw function
    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)


# Ball Class
class Ball:

    # Constructor
    def __init__(self, x, y, radius):
        self.rect = pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)
        self.speed_x = 4
        self.speed_y = 4

    # Move function
    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    # Draw function
    def draw(self, screen):
        pygame.draw.ellipse(screen, WHITE, self.rect)

    # Reset function
    def reset(self, x, y):
        self.rect.x = x
        self.rect.y = y
        self.speed_x *= -1
        self.speed_y *= -1

