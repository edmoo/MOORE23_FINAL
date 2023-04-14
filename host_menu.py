import pygame
from const import *

# Create the login button
back_button = pygame.Rect(WIDTH // 4, HEIGHT // 1.5, WIDTH // 2, 32)

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
        host_text = font.render("FEN:", True, BLACK)
        surface.blit(host_text, (WIDTH // 4 - host_text.get_width() - 16, HEIGHT // 3 + 8))
        
        # Draw the password field
        pygame.draw.rect(surface, COLOUR_TWO, start_field)
        start_text = font.render("Start", True, BLACK)
        surface.blit(start_text, (WIDTH // 4 - start_text.get_width() // 2, HEIGHT // 2 + 8))
        
        # Draw the login button
        pygame.draw.rect(surface, COLOUR_TWO, back_button)
        back_text = font.render("Back", True, BLACK)
        surface.blit(back_text, (WIDTH // 2 - back_text.get_width() // 2, HEIGHT // 1.5 + 8))

        surface.blit(text_surface, (host_field.x+5, host_field.y+5))

        text_surface = base_font.render(REN, True, (0, 0, 0))

        ip_surface = font.render(host_ip, True, BLACK)
        surface.blit(ip_surface, (10, 10))  #host can see their ip in the top left
