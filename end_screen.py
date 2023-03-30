import pygame
from const import *

pygame.font.init()


# Create the login button
continue_button = pygame.Rect(WIDTH // 4, HEIGHT // 1.5, WIDTH // 2, 32)
# Create the font for the username and password fields
font = font = pygame.font.SysFont("Arial", 32)
base_font = pygame.font.Font(None, 32)

# Create the username and password fields
stats_field = pygame.Rect(WIDTH // 4, HEIGHT // 2, WIDTH // 2, 32)



class EndScreen:

    def __init__(self):
        pass

    #show methods

    def show_screen(self, surface, board):
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        # Clear the surface
        surface.fill(WHITE)

        result = board.result
        if result == "1-0":
            victor_text = font.render("WHITE WINS!", True, BLACK)
        elif result == "0-1":
            victor_text = font.render("BLACK WINS!", True, BLACK)
        else:
            victor_text = font.render("DRAW!", True, BLACK)

        surface.blit(victor_text, (WIDTH // 4, HEIGHT // 3 + 8))
        
        # Draw the password field
        noTurns = str(board.halfmove_clock)
        statText = "No. Turns: "+ noTurns
        pygame.draw.rect(surface, BLACK, stats_field, 2)
        start_text = font.render(statText, True, BLACK)
        surface.blit(start_text, (WIDTH // 4 - start_text.get_width() // 2, HEIGHT // 2 + 8))
        
        # Draw the login button
        pygame.draw.rect(surface, BLACK, continue_button, 2)
        back_text = font.render("Continue", True, BLACK)
        surface.blit(back_text, (WIDTH // 2 - back_text.get_width() // 2, HEIGHT // 1.5 + 8))
