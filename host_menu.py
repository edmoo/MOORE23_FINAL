import pygame
from const import *

pygame.font.init()


# Create the login button
back_button = pygame.Rect(WIDTH // 4, HEIGHT // 1.5, WIDTH // 2, 32)
# Create the font for the username and password fields
font = font = pygame.font.SysFont("Arial", 32)
base_font = pygame.font.Font(None, 32)

# Create the username and password fields
host_field = pygame.Rect(WIDTH // 4, HEIGHT // 3, WIDTH // 2, 32)
password_field = pygame.Rect(WIDTH // 4, HEIGHT // 2, WIDTH // 2, 32)



class HostMenu:

    def __init__(self):
        pass

    #show methods

    def show_screen(self, surface):
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)

        # Clear the surface
        surface.fill(WHITE)

        # Draw the username field
        pygame.draw.rect(surface, BLACK, host_field, 2)
        host_text = font.render("REN:", True, BLACK)
        surface.blit(host_text, (WIDTH // 4 - host_text.get_width() - 16, HEIGHT // 3 + 8))
        
        # Draw the password field
        pygame.draw.rect(surface, BLACK, password_field, 2)
        password_text = font.render("Join", True, BLACK)
        surface.blit(password_text, (WIDTH // 4 - password_text.get_width() // 2, HEIGHT // 2 + 8))
        
        # Draw the login button
        pygame.draw.rect(surface, BLACK, back_button, 2)
        back_text = font.render("Back", True, BLACK)
        surface.blit(back_text, (WIDTH // 2 - back_text.get_width() // 2, HEIGHT // 1.5 + 8))