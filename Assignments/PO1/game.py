"""
Author: Kyle Gordon
Email: kylekgordon@gmail.com
Label: P01
Title: 2048x
Course: CMPS 5443
Semester: Spring 2023

Description:
    This program is a remake of the game 2048. The default size of the board is
    a 4 x 4 as the original game is. Tiles are moved and combined using the
    arrow keys. A bomb tile becomes available after 30 secs, which allows the
    player to blow up a tile of choosing. If no moved are left game is over and
    score saved.

Files:
    game.py : Driver Program
"""

import pygame
import random
import math

''' References
https://www.youtube.com/watch?v=rp9s1O3iSEQ&t=428s
https://www.youtube.com/watch?v=f29ZOu4rXlM

'''

# Variables
timer = pygame.time.Clock()
fps = 60
rows = 4
cols = 4
score = 0
time_elapse = 3000
new_play = True
bomb_clicked = False
card_clicked = False
game_over = False
spawn_card = True
first_guess_num = 0
second_guess_num = 0
init_count = 0
direction = ''

board = [[0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]]

correct = [[0, 0, 0, 0],
           [0, 0, 0, 0],
           [0, 0, 0, 0],
           [0, 0, 0, 0]]

spaces = []
used = []
option_list = []
pygame.font.init()
title_font = pygame.font.Font(r'Roboto-Bold.ttf', 56)
small_font = pygame.font.Font(r'Roboto-Bold.ttf', 50)
smaller_font = pygame.font.Font(r'Roboto-Bold.ttf', 30)

# 2048 game color library
colors = {0: (204, 192, 179),
          2: (238, 228, 218),
          4: (237, 224, 200),
          8: (242, 177, 121),
          16: (245, 149, 99),
          32: (246, 124, 95),
          64: (246, 94, 59),
          128: (237, 207, 114),
          256: (237, 204, 97),
          512: (237, 200, 80),
          1024: (237, 197, 63),
          2048: (237, 194, 46),
          'light text': (249, 246, 242),
          'dark text': (119, 110, 101),
          'other': (0, 0, 0),
          'bg': (187, 173, 160)}

# Create a bomb
bomb = pygame.image.load("assets/bomb.png")
bomb = pygame.transform.scale(bomb, (64, 64))
bombAvailable = False

# Create screen
screen = pygame.display.set_mode((306, 454))
pygame.display.set_caption('2048x')


def take_turn(direc, board_val):

    """Take your turn based on arrow keys. Tiles move to the
        direction of arrow keys pressed

        Params:
        Returns:
    """

    merged = [[False, False, False, False],
              [False, False, False, False],
              [False, False, False, False],
              [False, False, False, False]]
    global score

    # UP ARROW
    if direc == 'UP':
        for i in range(rows):
            for j in range(cols):
                shift = 0
                if i > 0:
                    for q in range(i):
                        if board_val[q][j] == 0:
                            shift += 1
                    if shift > 0:
                        board_val[i - shift][j] = board_val[i][j]
                        board_val[i][j] = 0
                    if board_val[i - shift - 1][j] == board_val[i - shift][j] \
                            and not merged[i - shift][j] and not merged[i - shift - 1][j]:
                        board_val[i - shift - 1][j] *= 2
                        score += board_val[i - shift - 1][j]
                        board_val[i - shift][j] = 0
                        merged[i - shift - 1][j] = True
    # DOWN ARROW
    elif direc == 'DOWN':
        for i in range(3):
            for j in range(4):
                shift = 0
                for q in range(i + 1):
                    if board_val[3 - q][j] == 0:
                        shift += 1
                if shift > 0:
                    board_val[2 - i + shift][j] = board_val[2 - i][j]
                    board_val[2 - i][j] = 0
                if 3 - i + shift <= 3:
                    if board_val[2 - i + shift][j] == board_val[3 - i + shift][j] and not merged[3 - i + shift][j] \
                            and not merged[2 - i + shift][j]:
                        board_val[3 - i + shift][j] *= 2
                        score += board_val[3 - i + shift][j]
                        board_val[2 - i + shift][j] = 0
                        merged[3 - i + shift][j] = True

    # LEFT ARROW
    elif direc == 'LEFT':
        for i in range(4):
            for j in range(4):
                shift = 0
                for q in range(j):
                    if board_val[i][q] == 0:
                        shift += 1
                if shift > 0:
                    board_val[i][j - shift] = board_val[i][j]
                    board_val[i][j] = 0
                if board_val[i][j - shift] == board_val[i][j - shift - 1] and not merged[i][j - shift - 1] \
                        and not merged[i][j - shift]:
                    board_val[i][j - shift - 1] *= 2
                    score += board_val[i][j - shift - 1]
                    board_val[i][j - shift] = 0
                    merged[i][j - shift - 1] = True
                    # print(merged)

    # RIGHT ARROW
    elif direc == 'RIGHT':
        for i in range(4):
            for j in range(4):
                shift = 0
                for q in range(j):
                    if board_val[i][3 - q] == 0:
                        shift += 1
                if shift > 0:
                    board_val[i][3 - j + shift] = board_val[i][3 - j]
                    board_val[i][3 - j] = 0
                if 4 - j + shift <= 3:
                    if board_val[i][4 - j + shift] == board_val[i][3 - j + shift] and not merged[i][4 - j + shift] \
                            and not merged[i][3 - j + shift]:
                        board_val[i][4 - j + shift] *= 2
                        score += board_val[i][4 - j + shift]
                        board_val[i][3 - j + shift] = 0
                        merged[i][4 - j + shift] = True

    return board_val


# Button classification for Bomb
class Button:
    def __init__(self, x, y):
        self.img = bomb
        self.rect = self.img.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self):
        global bomb_clicked
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True
                bomb_clicked = True
                #print("BombClicked")
            if not pygame.mouse.get_pressed()[0]:
                self.clicked = False
        screen.blit(self.img, (self.rect.x, self.rect.y))


def draw_background():
    """ This function creates a top header with text 2048x

        Params:
        Returns:
    """
    top_menu = pygame.draw.rect(screen, colors['bg'], [0, 0, 306, 74], 0, 10)
    title_text = title_font.render('2048x', True, (0, 0, 0))
    screen.blit(title_text, (75, 10))


def new_card(board_val):
    """ This function creates the card number at random and creates random new card

        Params: board_val
        Returns: board_val, board_full
    """
    count = 0
    board_full = False
    while any(0 in row for row in board_val) and count < 1:
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        if board_val[row][col] == 0:
            count += 1
            if random.randint(1, 10) == 10:
                board_val[row][col] = 4
            else:
                board_val[row][col] = 2
    if count < 1:
        board_full = True

    return board_val, board_full


def draw_cards(board_val):
    """ This function create background and the cards. Changes the color of
        the card and text based on the number value.

        Params: board_val
        Returns: card_list
    """
    card_list = []
    for i in range(rows):
        for j in range(cols):
            value = board_val[i][j]

            if value > 8:
                value_color = colors['light text']
            else:
                value_color = colors['dark text']
            if value <= 2048:
                color = colors[value]
            else:
                color = colors['other']
            card = pygame.draw.rect(screen, color, [j * 74 + 10, i * 74 + 84, 64, 64], 0, 5)
            card_list.append(card)
            if value > 0:
                value_len = len(str(value))
                font = pygame.font.Font('sans.ttf', 48 - (5 * value_len))
                value_text = font.render(str(value), True, value_color)
                text_rect = value_text.get_rect(center=(j * 74 + 42, i * 74 + 115))
                screen.blit(value_text, text_rect)
                pygame.draw.rect(screen, (0, 255, 0), [j * 74 + 8, i * 74 + 82, 69, 69], 3, 4)

    return card_list


# draw scores text on board
def draw_score():
    score_text = small_font.render(f'Score: {score}', True, 'white')
    screen.blit(score_text, (10, 390))


def reset_card(card_num):
    """ This function takes in index position after mouse clicked
        then calculates actual location in array and resets it to zero.
        This will complete the bomb play.

        Params: card_num
        Returns: board, score
    """
    global board
    global score
    print(board)
    print(card_num)
    target_x = card_num // 4
    target_y = card_num % 4
    print(target_x)
    print(int(target_y))
    board[target_x][target_y] = 0
    score -= 10
    print(board)


bombX = 240
bombY = 5

bombCard = Button(bombX, bombY)

# Game loop
running = True

while running:
    timer.tick(fps)
    screen.fill((0, 0, 0))

    if not bombAvailable:
        time_elapse -= 1

    board1 = draw_cards(board)
    draw_background()
    draw_score()
    # print(board1)

    if spawn_card or init_count < 2:
        board, game_over = new_card(board)
        spawn_card = False
        init_count += 1

    if direction != '':
        board = take_turn(direction, board)
        direction = ''
        spawn_card = True

    if bomb_clicked and card_clicked:
        # print("Card Reset")
        reset_card(card_clicked_num)

        time_elapse = 3000
        bomb_clicked = False
        card_clicked = False
        bombAvailable = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                direction = 'UP'
            elif event.key == pygame.K_DOWN:
                direction = 'DOWN'
            elif event.key == pygame.K_LEFT:
                direction = 'LEFT'
            elif event.key == pygame.K_RIGHT:
                direction = 'RIGHT'

        if event.type == pygame.MOUSEBUTTONDOWN:
            m_x, m_y = pygame.mouse.get_pos()
            for i in range(len(board1)):
                button = board1[i]
                if not game_over and bomb_clicked:
                    if button.collidepoint(event.pos) and not card_clicked:
                        card_clicked = True
                        card_clicked_num = i
                        print(first_guess_num)

    # print(board)
    if time_elapse == 0:
        bombCard.draw()
        bombAvailable = True
    clock_text = smaller_font.render(f'{math.trunc(time_elapse/100)}', True, (0, 255, 255))
    screen.blit(clock_text, (253, 25))
    pygame.display.update()

pygame.quit()
