import pygame
from const import *

pygame.font.init()


# Create the login button
back_button = pygame.Rect(WIDTH // 4, HEIGHT // 1.5, WIDTH // 2, 32)
# Create the font for the username and password fields
font = font = pygame.font.SysFont("Arial", 32)
base_font = pygame.font.Font(None, 32)

# Create the username and password fields
client_field = pygame.Rect(WIDTH // 4, HEIGHT // 3, WIDTH // 2, 32)
join_field = pygame.Rect(WIDTH // 4, HEIGHT // 2, WIDTH // 2, 32)



class ClientMenu:

    def __init__(self):
        pass

    #show methods

    def show_screen(self, surface):
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        # Clear the surface
        surface.fill(WHITE)

        # Draw the username field
        pygame.draw.rect(surface, BLACK, client_field, 2)
        client_text = font.render("IP:", True, BLACK)
        surface.blit(client_text, (WIDTH // 4 - client_text.get_width() - 16, HEIGHT // 3 + 8))
        
        # Draw the password field
        pygame.draw.rect(surface, BLACK, join_field, 2)
        join_text = font.render("Join", True, BLACK)
        surface.blit(join_text, (WIDTH // 4 - join_text.get_width() // 2, HEIGHT // 2 + 8))
        
        # Draw the login button
        pygame.draw.rect(surface, BLACK, back_button, 2)
        back_text = font.render("Back", True, BLACK)
        surface.blit(back_text, (WIDTH // 2 - back_text.get_width() // 2, HEIGHT // 1.5 + 8))