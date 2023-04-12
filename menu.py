import pygame
from const import *

pygame.font.init()


# Create the login button
host_button = pygame.Rect(WIDTH // 4, HEIGHT // 3, WIDTH // 2, 32)
# Create the font for the username and password fields
font = font = pygame.font.SysFont("Arial", 32)
base_font = pygame.font.Font(None, 32)

# Create the username and password fields
quit_field = pygame.Rect(WIDTH // 4, HEIGHT // 1.5, WIDTH // 2, 32)
join_field = pygame.Rect(WIDTH // 4, HEIGHT // 2, WIDTH // 2, 32)



class Menu:

    def __init__(self):
        pass

    #show methods

    def show_screen(self, surface):

        # Clear the surface
        surface.fill(COLOUR_ONE)

        # Draw the username field
        pygame.draw.rect(surface, COLOUR_TWO, host_button, 2)
        host_text = font.render("Host", True, COLOUR_TWO)
        surface.blit(host_text, (WIDTH // 4 - host_text.get_width() // 2, HEIGHT // 3 + 8))
        
        # Draw the password field
        pygame.draw.rect(surface, COLOUR_TWO, join_field, 2)
        password_text = font.render("Join", True, COLOUR_TWO)
        surface.blit(password_text, (WIDTH // 4 - password_text.get_width() // 2, HEIGHT // 2 + 8))
        
        # Draw the login button
        pygame.draw.rect(surface, COLOUR_TWO, quit_field, 2)
        quit_text = font.render("Quit", True, COLOUR_TWO)
        surface.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 1.5 + 8))
