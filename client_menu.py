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

    def show_screen(self, surface, ipInput):

        # Clear the surface
        surface.fill(COLOUR_ONE)
        text_surface = base_font.render(ipInput, True, (0, 0, 0))

        # Draw the username field
        pygame.draw.rect(surface, COLOUR_TWO, client_field, 2)
        client_text = font.render("IP:", True, COLOUR_TWO)
        surface.blit(client_text, (WIDTH // 4 - client_text.get_width() - 16, HEIGHT // 3 + 8))
        
        # Draw the password field
        pygame.draw.rect(surface, COLOUR_TWO, join_field, 2)
        join_text = font.render("Join", True, COLOUR_TWO)
        surface.blit(join_text, (WIDTH // 4 - join_text.get_width() // 2, HEIGHT // 2 + 8))
        
        # Draw the login button
        pygame.draw.rect(surface, COLOUR_TWO, back_button, 2)
        back_text = font.render("Back", True, COLOUR_TWO)
        surface.blit(back_text, (WIDTH // 2 - back_text.get_width() // 2, HEIGHT // 1.5 + 8))

        surface.blit(text_surface, (client_field.x+5, client_field.y+5))