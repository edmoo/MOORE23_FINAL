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
start_field = pygame.Rect(WIDTH // 4, HEIGHT // 2, WIDTH // 2, 32)



class HostMenu:

    def __init__(self):
        pass

    #show methods

    def show_screen(self, surface, REN, host_ip):
        # Clear the surface
        surface.fill(COLOUR_ONE)
        text_surface = base_font.render(REN, True, (0, 0, 0))

        # Draw the username field
        pygame.draw.rect(surface, COLOUR_TWO, host_field, 2)
        host_text = font.render("FEN:", True, COLOUR_TWO)
        surface.blit(host_text, (WIDTH // 4 - host_text.get_width() - 16, HEIGHT // 3 + 8))
        
        # Draw the password field
        pygame.draw.rect(surface, COLOUR_TWO, start_field, 2)
        start_text = font.render("Start", True, COLOUR_TWO)
        surface.blit(start_text, (WIDTH // 4 - start_text.get_width() // 2, HEIGHT // 2 + 8))
        
        # Draw the login button
        pygame.draw.rect(surface, COLOUR_TWO, back_button, 2)
        back_text = font.render("Back", True, COLOUR_TWO)
        surface.blit(back_text, (WIDTH // 2 - back_text.get_width() // 2, HEIGHT // 1.5 + 8))

        surface.blit(text_surface, (host_field.x+5, host_field.y+5))

        text_surface = base_font.render(REN, True, (0, 0, 0))

        ip_surface = font.render(host_ip, True, COLOUR_TWO)
        surface.blit(ip_surface, (10, 10))  #host can see their ip in the top left
