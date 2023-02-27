import pygame
import math
import random
from pygame.math import Vector2

# Initialize Pygame
pygame.init()
timer = pygame.time.Clock()
time_elapse = 1500
fps = 60
pygame.font.init()
pygame.mixer.get_init()

# Display Settings
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("War On Apes")

# Color library
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)

# Set up the fonts
small_font = pygame.font.Font(r'assets/misc/Roboto-Bold.ttf', 50)
smaller_font = pygame.font.Font(r'assets/misc/Roboto-Bold.ttf', 30)

# Game Variables
gravity = 9.81
power = 50
angle = 45
player1_score = 0
player2_score = 0
turn = 1
wind = random.randint(-5, 5)

# Find Sprite Height and Width
# bazooka1 = pygame.image.load("assets/sprites/banana.png")
# bazooka1_rect1 = bazooka1.get_rect()
# print(bazooka1_rect1.h)
# print(bazooka1_rect1.w)


class Monkey(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/sprites/monkey.png")
        self.rect = self.image.get_rect()
        self.position = position
        self.time_to_fire = 14
        self.damage = 0
        self.damaged = False
        self.score = 0

        if self.position == "left":
            self.rect.center = (200, 500)
            self.image = pygame.transform.flip(self.image, 1, 0)
        elif self.position == "right":
            self.rect.center = (500, 500)

    def move(self, direction):
        if direction == "left":
            self.rect.x -= 5
        elif direction == "right":
            self.rect.x += 5


# Set up the sprites
class Bazooka(pygame.sprite.Sprite):
    def __init__(self, position, x, y):
        super().__init__()
        self.image = pygame.image.load('assets/sprites/bazooka.png')
        self.image = pygame.transform.scale(self.image, (513/6, 129/6))
        self.rect = self.image.get_rect()
        self.position = position
        self.pos = Vector2(x, y)
        self.angle = 0
        if self.position == "left":
            self.rect.center = (x+10, y+8)
        elif self.position == "right":
            self.rect.center = (x-10, y+8)
            self.image = pygame.transform.flip(self.image, 1, 0)
        self.base_image = self.image

    def rotate(self, direction):
        self.angle += direction
        if self.angle > 90:
            self.angle = 90
        elif self.angle < 0:
            self.angle = 0

        if self.position == "left":
            old_rect = self.rect.bottomleft
            self.image = pygame.transform.rotate(self.base_image, self.angle)
            self.rect = self.image.get_rect()
            self.rect.bottomleft = old_rect
        elif self.position == "right":
            old_rect = self.rect.bottomright
            self.image = pygame.transform.rotate(self.base_image, 0 - self.angle)
            self.rect = self.image.get_rect()
            self.rect.bottomright = old_rect

    def move(self, direction):
        if direction == "left":
            self.rect.x -= 5
        elif direction == "right":
            self.rect.x += 5


class Banana(pygame.sprite.Sprite):
    def __init__(self, position, v, theta, x, y):
        super().__init__()
        self.image = pygame.image.load('assets/sprites/Banana.png')
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.v = v
        self.position = position
        self.theta = math.radians(theta)
        self.vx = self.v * math.cos(self.theta)
        self.vy = self.v * math.sin(self.theta)
        self.dx = 0
        self.dy = 0
        self.t = 0
        self.g = -2
        self.scored = False

    def update(self):
        if self.position == "left":
            self.rect.x = player1_bazooka.rect.x + int(self.vx * self.t)
            self.rect.y = int(player1_bazooka.rect.y - self.vy * self.t - 0.5 * self.g * self.t**2)
            self.t += 0.1
            # print(self.rect.x)
            # print(self.rect.y)

            # Collision Detection
            if self.rect.colliderect(player2.rect) and not self.scored:
                self.scored = True
                player1.score += 1
                print("Player1 Score: ", player1.score)

        elif self.position == "right":
            self.rect.x = player2_bazooka.rect.x - int(self.vx * self.t)
            self.rect.y = int(player2_bazooka.rect.y - self.vy * self.t - 0.5 * self.g * self.t**2)
            self.t += 0.1

            # Collision Detection
            if self.rect.colliderect(player1.rect) and not self.scored:
                self.scored = True
                player2.score += 1
                print("Player2 Score: ", player2.score)

        # check for out of bounds
        if self.rect.x > screen_width or self.rect.y > screen_height:
            self.kill()


def fire_banana():
    pygame.mixer.music.stop()
    pygame.mixer.Sound("assets/sound/gun.ogg")


def player_turn(p_turn):
    if p_turn == 1:
        player_1 = smaller_font.render(f'Player: {p_turn}', True, black)
        screen.blit(player_1, (350, 75))
    elif p_turn == 2:
        player_2 = smaller_font.render(f'Player: {p_turn}', True, black)
        screen.blit(player_2, (350, 75))


# draw scores text on board
def draw_score():
    score_text1 = smaller_font.render("Score: {}".format(player1.score), True, red)
    screen.blit(score_text1, (75, 10))
    score_text2 = smaller_font.render("Score: {}".format(player2.score), True, red)
    screen.blit(score_text2, (600, 10))


# Draw the mountain
mountain_points = [(200, 500), (700 * 0.2, 500 * 0.6),
                   (700 * 0.4, 500 * 0.8), (700 * 0.6, 200 * 0.6),
                   (700 * 0.8, 500 * 0.9), (700, 500)]

# Draw the trees

trees = pygame.image.load('assets/sprites/trees/tree1/tree1_00.png')
trees = pygame.transform.scale(trees, (64, 64))
tree_positions = [(50, screen_height * 0.8), (150, screen_height * 0.7), (250, screen_height * 0.9),
                  (350, screen_height * 0.6), (450, screen_height * 0.8), (550, screen_height * 0.7)]

# trees.rect(0, 0)

# Set up the groups
player1 = Monkey("left")
player2 = Monkey("right")
player1_bazooka = Bazooka("left", 200, 500)
player2_bazooka = Bazooka("right", 500, 500)

all_sprites = pygame.sprite.Group()
all_sprites.add(player1)
all_sprites.add(player2)
all_sprites.add(player1_bazooka)
all_sprites.add(player2_bazooka)

banana_sprite = pygame.sprite.Group()

# Game loop
running = True
while running:
    timer.tick(fps)
    time_elapse -= 1


    if time_elapse == 0:
        if turn == 1:
            player1_banana = Banana("left", player1_bazooka.angle, 45, player1.rect.x, player1.rect.y)
            banana_sprite.add(player1_banana)
            all_sprites.add(player1_banana)

        elif turn == 2:
            player2_banana = Banana("right", player2_bazooka.angle, 45, 500, 500)
            banana_sprite.add(player2_banana)
            all_sprites.add(player2_banana)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if turn == 1:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_UP:
                    player1_bazooka.rotate(1)
                elif event.key == pygame.K_DOWN:
                    player1_bazooka.rotate(-1)
                elif event.key == pygame.K_LEFT:
                    player1.move("left")
                    player1_bazooka.move("left")
                elif event.key == pygame.K_RIGHT:
                    player1.move("right")
                    player1_bazooka.move("right")
            elif turn == 2:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_UP:
                    player2_bazooka.rotate(1)
                elif event.key == pygame.K_DOWN:
                    player2_bazooka.rotate(-1)
                elif event.key == pygame.K_LEFT:
                    player2.move("left")
                    player2_bazooka.move("left")
                elif event.key == pygame.K_RIGHT:
                    player2.move("right")
                    player2_bazooka.move("right")


                # if turn == 1:
                #     player1_cannon.rotate("up")
                # elif turn == 2:
                #     player1_cannon.rotate("down")
                # if event.key == pygame.K_SPACE:
                #     all_sprites.add(Cannon(player1_cannon.rect.center))
    if time_elapse == 0:
        if turn == 1:
            fire_banana()
            turn = 2
            time_elapse = 1500

        elif turn == 2:
            fire_banana()
            time_elapse = 1500
            turn = 1

    all_sprites.update()
    screen.fill(white)
    #screen.blit(monkey1, monkey_rect1, (0, 0, 100, 100))
    pygame.draw.rect(screen, (255, 0, 0), (0, 500, 800, 100))
    pygame.draw.polygon(screen, green, mountain_points)
    all_sprites.draw(screen)
    clock_text = small_font.render(f'{math.trunc(time_elapse/100)}', True, blue)
    screen.blit(clock_text, (375, 10))
    draw_score()
    player_turn(turn)
    pygame.display.update()


pygame.quit()
exit()
