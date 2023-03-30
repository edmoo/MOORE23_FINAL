import pygame
from const import *

pygame.font.init()


lobback_button = pygame.Rect(WIDTH // 4, HEIGHT // 1.5, WIDTH // 2, 32)

font = font = pygame.font.SysFont("Arial", 32)
base_font = pygame.font.Font(None, 32)




class JoinLobby:

    def __init__(self):
        pass

    #show methods

    def show_screen(self, surface):
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        # Clear the surface
        surface.fill(WHITE)

        

        start_text = font.render("Waiting for host to start...", True, BLACK)
        surface.blit(start_text, (WIDTH // 4 - start_text.get_width() // 2, HEIGHT // 2 + 8))
        
        # Draw the login button
        pygame.draw.rect(surface, BLACK, lobback_button, 2)
        back_text = font.render("Back", True, BLACK)
        surface.blit(back_text, (WIDTH // 2 - back_text.get_width() // 2, HEIGHT // 1.5 + 8))

