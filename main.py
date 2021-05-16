import time
import sys
import os
import pygame
import random
from pygame import mixer

# FILE DIRECTORIES
FOLDER_DIRECTORY = os.path.dirname(sys.argv[0])
BIRD_IMAGE_DIRECTORY = os.path.join(FOLDER_DIRECTORY, 'data', 'macaw.png')
BIRD_IMAGE = pygame.transform.flip(pygame.image.load(BIRD_IMAGE_DIRECTORY), True, False)
BIRD_HEIGHT = BIRD_IMAGE.get_height()-21
BIRD_WIDTH = BIRD_IMAGE.get_width()

# INITIALIZE GAME
pygame.init()
game_run = True
clock = pygame.time.Clock()

# AUDIOS
mixer.init()
bell = mixer.Sound(os.path.join(FOLDER_DIRECTORY, "data", "ding.mp3"))
flap = mixer.Sound(os.path.join(FOLDER_DIRECTORY, "data", "flap.mp3"))
crash = mixer.Sound(os.path.join(FOLDER_DIRECTORY, "data", "crash.mp3"))
bell.set_volume(.05)
flap.set_volume(.1)
crash.set_volume(.4)

# GAME WINDOW SETTINGS
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

pygame.display.set_caption('Flappy Bird')

score = 0

#FONTS
font = pygame.font.SysFont('Comic Sans MS', 64)

class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.acceleration_y = .4
        self.velocity_y = 0
        self.hitbox = pygame.Rect(x, y+10, BIRD_WIDTH, BIRD_HEIGHT)

    def draw_hitbox(self):
        pygame.draw.rect(WINDOW, (255, 0, 0), self.hitbox, 2)
    
player = Bird(100, 300)

class Obstacle:
    def __init__(self, h, x, y):
        self.rect = (x, y, 80, h)
        self.hitbox = pygame.Rect(x, y, 80, h)
        self.velocity_x = 2

    def draw(self):
        pygame.draw.rect(WINDOW, (255, 255, 255), self.rect)

obstacle_list = []
for i in range(1, 5):
    rand = random.randint(50, 450)
    obstacle_list.append(Obstacle(rand, i*250+100, 0))
    obstacle_list.append(Obstacle(500, i*250+100, rand+150))


# RENDER WINDOW
def redraw_window():

    WINDOW.fill((0, 0, 0))
    WINDOW.blit(BIRD_IMAGE, (player.x, player.y))
    for obstacle in obstacle_list:
        obstacle.draw()
    score_text = font.render(str(int(score)), True, (255, 0, 0))
    WINDOW.blit(score_text, (370, 100))
    # player.draw_hitbox()
    pygame.display.update()
    if lose:
        time.sleep(1)

lose = False

def reset_game():
    global lose, score
    score = 0
    lose = False
    obstacle_list.clear()
    for i in range(1, 5):
        rand = random.randint(50, 450)
        obstacle_list.append(Obstacle(rand, i*250+100, 0))
        obstacle_list.append(Obstacle(500, i*250+100, rand+150))
    player.x = 100
    player.y = 300
    player.velocity_y = -6

while game_run:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not lose:
                    player.velocity_y = -6
                    flap.play()
                else:
                    reset_game()
    if lose:
        continue

    # UPDATE PLAYER POSITION AND HITBOX
    player.y = max(0, min(player.y+player.velocity_y, WINDOW_HEIGHT - BIRD_HEIGHT))
    player.velocity_y += player.acceleration_y
    player.hitbox = pygame.Rect(player.x, player.y+10, BIRD_WIDTH, BIRD_HEIGHT)

    # UPDATE POSITION OF EACH OBSTACLE
    for obstacle in obstacle_list:
        obstacle.rect = (obstacle.rect[0] - obstacle.velocity_x, obstacle.rect[1], obstacle.rect[2], obstacle.rect[3])
        obstacle.hitbox = pygame.Rect(obstacle.rect[0], obstacle.rect[1], obstacle.rect[2], obstacle.rect[3])

    # POP THE FIRST PAIR OF OBSTACLES IF OFFSCREEN AND APPENDS A NEW ONE
    furthest_x = obstacle_list[-1].rect[0]
    for i in range(2):
        obstacle = obstacle_list[i]
        if obstacle.rect[0] < -80:
            obstacle_list.pop(obstacle_list.index(obstacle))
            rand = random.randint(50, 450)
            obstacle_list.append(Obstacle(rand, furthest_x + 250, 0))
            obstacle_list.append(Obstacle(500, furthest_x + 250, rand+150))

    # CHECKS COLLISION
    for i in range(4):
        if player.x - obstacle_list[i].rect[0] == 30:
            bell.play() 
            score += .5
        if obstacle_list[i].hitbox.colliderect(player.hitbox) or player.y + BIRD_HEIGHT == WINDOW_HEIGHT:
            crash.play()
            lose = True
            break

    redraw_window()
