import pygame

# initialize pygame
pygame.init()


def selectGame ():

    # define some colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    # set up the screen
    screen_width = 640
    screen_height = 480
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Game Selection Screen")

    # set up the font
    font = pygame.font.SysFont(None, 40)

    # create the solo button
    solo_button_width = 200
    solo_button_height = 50
    solo_button_x = (screen_width - solo_button_width) // 2
    solo_button_y = (screen_height - solo_button_height) // 2 - 50
    solo_button_rect = pygame.Rect(solo_button_x, solo_button_y, solo_button_width, solo_button_height)

    # create the multiplayer button
    multiplayer_button_width = 200
    multiplayer_button_height = 50
    multiplayer_button_x = (screen_width - multiplayer_button_width) // 2
    multiplayer_button_y = (screen_height - multiplayer_button_height) // 2 + 50
    multiplayer_button_rect = pygame.Rect(multiplayer_button_x, multiplayer_button_y, multiplayer_button_width, multiplayer_button_height)

    # main game loop
    while True:
        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # check if the solo button is clicked
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if solo_button_rect.collidepoint(mouse_pos):
                    from game2 import Spacers
                    spacers = Spacers()
                    spacers.main_loop(True)
                    print("Solo button clicked!")
                    # launch solo game mode here

            # check if the multiplayer button is clicked
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if multiplayer_button_rect.collidepoint(mouse_pos):
                    from game import Spacers
                    spacers = Spacers()
                    spacers.main_loop(True)
                    print("Multiplayer button clicked!")
                    # launch multiplayer game mode here

        # draw the buttons
        pygame.draw.rect(screen, WHITE, solo_button_rect)
        text = font.render("Solo", True, BLACK)
        text_rect = text.get_rect(center=solo_button_rect.center)
        screen.blit(text, text_rect)

        pygame.draw.rect(screen, WHITE, multiplayer_button_rect)
        text = font.render("Multiplayer", True, BLACK)
        text_rect = text.get_rect(center=multiplayer_button_rect.center)
        screen.blit(text, text_rect)

        # update the display
        pygame.display.update()