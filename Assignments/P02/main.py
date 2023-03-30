import pygame
import math
import random
from pygame.math import Vector2

from floor import Ground

# Initialize Pygame
pygame.init()
timer = pygame.time.Clock()
time_elapse = 1000
fps = 60
pygame.font.init()
pygame.mixer.get_init()
paused = False

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
big_font = pygame.font.Font(r'assets/misc/Roboto-Bold.ttf', 75)
bigger_font = pygame.font.Font(r'assets/misc/Roboto-Bold.ttf', 90)

# Game Variables
gravity = 0.01  # gravity
power = 50
angle = 45
player1_score = 0
player2_score = 0
turn = 1
player1_start_x = 200
player1_start_y = 480
player2_start_x = 500
player2_start_y = 480

wind = random.randint(-5, 5)


class Monkey(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/sprites/monkey.png")
        self.rect = self.image.get_rect()
        self.position = position
        self.time_to_fire = 14
        self.damage = 0
        self.damaged = False
        self.score = 9
        self.speed = 0

        if self.position == "left":
            self.rect.center = (player1_start_x, player1_start_y)
            self.image = pygame.transform.flip(self.image, 1, 0)
        elif self.position == "right":
            self.rect.center = (player2_start_x, player2_start_y)

    def move(self, direction):
        if direction == "left":
            self.rect.x -= 5
        elif direction == "right":
            self.rect.x += 5

    # def update(self):

        # if self.rect.y > 504:
        #     self.rect.y = 400
        #     self.speed = 0

        # if player1.rect.y > 504:
        #     player1.rect.y = 400

        # # Check if there is the monkey collides with any of bricks
        # brick_collision_list = pygame.sprite.spritecollide(self, all_bricks, False)
        # for brick in brick_collision_list:
        #     # if self.rect.colliderect(brick.rect):
        #     self.rect.center = (self.rect.x, brick.rect.top - 40)


# Set up the sprites
class Bazooka(pygame.sprite.Sprite):
    def __init__(self, position, x, y):
        super().__init__()
        self.image = pygame.image.load('assets/sprites/bazooka.png')
        self.image = pygame.transform.scale(self.image, (513 / 6, 129 / 6))
        self.rect = self.image.get_rect()
        self.position = position
        self.pos = Vector2(x, y)
        self.angle = 0
        if self.position == "left":
            self.rect.center = (x + 10, y + 8)
        elif self.position == "right":
            self.rect.center = (x - 10, y + 8)
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
            self.rect.x = (513 / 6) + player1_bazooka.rect.x + int(self.vx * self.t)
            self.rect.y = int(player1_bazooka.rect.y - self.vy * self.t - 0.5 * self.g * self.t ** 2)
            self.t += 0.1

            # Collision Detection
            if self.rect.colliderect(player2.rect) and not self.scored:
                self.scored = True
                player1.score += 1
                print("Player1 Score: ", player1.score)

        elif self.position == "right":
            self.rect.x = player2_bazooka.rect.x - int(self.vx * self.t)
            self.rect.y = int(player2_bazooka.rect.y - self.vy * self.t - 0.5 * self.g * self.t ** 2)
            self.t += 0.1

            # Collision Detection
            if self.rect.colliderect(player1.rect) and not self.scored:
                self.scored = True
                player2.score += 1
                print("Player2 Score: ", player2.score)

        brick_collision_list = pygame.sprite.spritecollide(self, all_bricks, False)
        for brick in brick_collision_list:
            brick.kill()
            self.kill()

        # check for out of bounds
        if self.rect.x > screen_width or self.rect.y > screen_height:
            self.kill()


def fire_banana():
    sound = pygame.mixer.Sound("assets/sound/gun.ogg")
    sound.play()
    pygame.mixer.music.stop()


def player_turn(p_turn):
    if p_turn == 1:
        player_1 = smaller_font.render(f'Player: {p_turn}', True, black)
        screen.blit(player_1, (350, 75))
    elif p_turn == 2:
        player_2 = smaller_font.render(f'Player: {p_turn}', True, black)
        screen.blit(player_2, (350, 75))


# def paused():
#     if player1.score == 10:
#         winning_text1 = big_font.render("Player 1 Won", True, red)
#         pause = True
#         while pause:
#             screen.fill(white)
#             screen.blit(winning_text1, (200, 200))
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     pygame.quit()
#                     quit()
#
#         pygame.display.update()
#
#     elif player2.score == 10:
#         winning_text1 = big_font.render("Player 2 Won", True, red)
#         pause = True
#         while pause:
#             screen.fill(white)
#             screen.blit(winning_text1, (200, 200))
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     pygame.quit()
#                     quit()
#
#         pygame.display.update()

def winner_screen():
    global paused
    if player1.score == 10:
        winning_text1 = big_font.render("Player 1 Won", True, red)
        screen.blit(winning_text1, (200, 200))
        paused = True

    elif player2.score == 10:
        winning_text1 = big_font.render("Player 2 Won", True, red)
        screen.blit(winning_text1, (200, 200))
        paused = True


def damage_bar():
    # Drawing Rectangle
    pygame.draw.rect(screen, red, pygame.Rect(75, 40, 100 - player2.score * 10, 20))
    pygame.draw.rect(screen, red, pygame.Rect(550, 40, 100 - player1.score * 10, 20))
    damage_text1 = smaller_font.render("Damage: {} % ".format(player2.score*10), True, blue)
    screen.blit(damage_text1, (75, 10))
    damage_text2 = smaller_font.render("Damage: {} %".format(player1.score*10), True, blue)
    screen.blit(damage_text2, (550, 10))

# draw scores text on board
# def draw_score():
#     score_text1 = smaller_font.render("Score: {}".format(player1.score), True, red)
#     screen.blit(score_text1, (75, 10))
#     score_text2 = smaller_font.render("Score: {}".format(player2.score), True, red)
#     screen.blit(score_text2, (600, 10))


# Draw the mountain
mountain_points = [(100, 500), (700 * 0.3, 500 * 0.6),
                   (700 * 0.4, 500 * 0.8), (700 * 0.6, 200 * 0.6),
                   (700 * 0.8, 500 * 0.9), (700, 500)]

# Draw the trees
trees = [pygame.image.load('assets/sprites/trees/tree1/tree1_00.png'),
         pygame.image.load('assets/sprites/trees/tree2/tree2_00.png'),
         pygame.image.load('assets/sprites/trees/tree3/tree3_00.png')]

number1 = random.randint(1, 50)
number2 = random.randint(50, 150)
number3 = random.randint(150, 250)
number4 = random.randint(250, 350)
number5 = random.randint(350, 450)
number6 = random.randint(450, 550)


def tree():
    tree_positions = [(number1, screen_height * 0.85), (number2, screen_height * 0.7), (number3, screen_height * 0.9),
                      (number4, screen_height * 0.6), (number5, screen_height * 0.85), (number6, screen_height * 0.7),
                      (300, screen_height * 0.85)]

    for tree_pos in tree_positions:
        for i in range(3):
            pygame.transform.scale(trees[i], (64, 64))
            screen.blit(trees[i], tree_pos)


# trees.rect(0, 0)

# Set up the groups
player1 = Monkey("left")
player2 = Monkey("right")
player1_bazooka = Bazooka("left", player1_start_x, player1_start_y)
player2_bazooka = Bazooka("right", player2_start_x, player2_start_y)
#player1_banana = Banana("left", player1_bazooka.angle, 45, player1.rect.x, player1.rect.y)
#player2_banana = Banana("right", player2_bazooka.angle, 45, player2.rect.x, player2.rect.y)


all_sprites = pygame.sprite.Group()
all_sprites.add(player1)
all_sprites.add(player2)
all_sprites.add(player1_bazooka)
all_sprites.add(player2_bazooka)

banana_sprite = pygame.sprite.Group()


# Create floor
all_bricks = pygame.sprite.Group()
for i in range(26):
    brick = Ground(red, 32, 32)
    brick.rect.x = 0 + i * 32
    brick.rect.y = 504
    all_sprites.add(brick)
    all_bricks.add(brick)
for i in range(26):
    brick = Ground(blue, 32, 32)
    brick.rect.x = 0 + i * 32
    brick.rect.y = 536
    all_sprites.add(brick)
    all_bricks.add(brick)
for i in range(26):
    brick = Ground(green, 32, 32)
    brick.rect.x = 0 + i * 32
    brick.rect.y = 568
    all_sprites.add(brick)
    all_bricks.add(brick)

# Game loop
running = True
game_over = False

while running:
    timer.tick(fps)
    time_elapse -= 1

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if turn == 1:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_w:
                    player1_bazooka.rotate(1)
                elif event.key == pygame.K_s:
                    player1_bazooka.rotate(-1)
                elif event.key == pygame.K_a:
                    player1.move("left")
                    player1_bazooka.move("left")
                elif event.key == pygame.K_d:
                    player1.move("right")
                    player1_bazooka.move("right")
                elif event.key == pygame.K_f:
                    player1_banana = Banana("left", player1_bazooka.angle, 45, player1.rect.x, player1.rect.y)
                    all_sprites.add(player1_banana)
                    banana_sprite.add(player1_banana)
                    fire_banana()
                    turn = 2
                    time_elapse = 1000

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
                elif event.key == pygame.K_RSHIFT:
                    player2_banana = Banana("right", player2_bazooka.angle, 45, player2.rect.x, player2.rect.y)
                    all_sprites.add(player2_banana)
                    banana_sprite.add(player2_banana)
                    fire_banana()
                    time_elapse = 1000
                    turn = 1

    if not paused and not game_over:
        if time_elapse == 0:
            if turn == 1:
                turn = 2
                time_elapse = 1000

            elif turn == 2:
                time_elapse = 1000
                turn = 1

        screen.fill(white)
        pygame.draw.polygon(screen, green, mountain_points)
        all_sprites.draw(screen)
        clock_text = small_font.render(f'{math.trunc(time_elapse / 100)}', True, blue)
        screen.blit(clock_text, (375, 10))
        damage_bar()
        winner_screen()
        # draw_score()
        tree()
        all_sprites.update()
        player_turn(turn)
        pygame.display.update()

pygame.quit()
exit()
