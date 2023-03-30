import pygame

# Initialize Pygame
pygame.init()

# Set the screen size and create a window
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Set the background color
bg_color = (135, 206, 250)

# Draw the mountain
mountain_color = (128, 128, 128)
mountain_points = [(0, screen_height), (screen_width * 0.2, screen_height * 0.6),
                   (screen_width * 0.4, screen_height * 0.8), (screen_width * 0.6, screen_height * 0.6),
                   (screen_width * 0.8, screen_height * 0.9), (screen_width, screen_height)]
pygame.draw.polygon(screen, mountain_color, mountain_points)

# Draw the trees
tree_color = (34, 139, 34)
tree_positions = [(50, screen_height * 0.8), (150, screen_height * 0.7), (250, screen_height * 0.9),
                  (350, screen_height * 0.6), (450, screen_height * 0.8), (550, screen_height * 0.7)]
for pos in tree_positions:
    pygame.draw.rect(screen, tree_color, pygame.Rect(pos[0], pos[1], 20, 40))
    pygame.draw.polygon(screen, tree_color, [(pos[0] - 30, pos[1]), (pos[0] + 10, pos[1] - 50),
                                             (pos[0] + 50, pos[1])])

# Update the display
pygame.display.update()

# Main loop to keep the window open
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Quit Pygame
pygame.quit()