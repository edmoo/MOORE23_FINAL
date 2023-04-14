import pygame
from const import *

# Create the login button
continue_button = pygame.Rect(WIDTH // 4, HEIGHT // 1.5, WIDTH // 2, 32)
toggle_button = pygame.Rect(WIDTH // 4, HEIGHT // 1.33, WIDTH //2, 32)

# Create the username and password fields
stats_field = pygame.Rect(WIDTH // 4, HEIGHT // 2, WIDTH // 2, 32)



class EndScreen:

    def __init__(self):
        pass

    #show methods

    def show_screen(self, surface, board, numTurns, toggleBoard):

        #clear surface
        surface.fill(COLOUR_ONE)

        result = board.result
        if result == "1-0":
            victor_text = font.render("WHITE WINS!", True, BLACK)
        elif result == "0-1":
            victor_text = font.render("BLACK WINS!", True, BLACK)
        else:
            victor_text = font.render("DRAW!", True, COLOUR_TWO)

        surface.blit(victor_text, (WIDTH // 4, HEIGHT // 3 + 8))
        
        #display number of turns taken
        statText = "No. Turns: "+ str(numTurns)
        pygame.draw.rect(surface, COLOUR_TWO, stats_field)
        start_text = font.render(statText, True, BLACK)
        surface.blit(start_text, (WIDTH // 4 - start_text.get_width() // 2, HEIGHT // 2 + 8))
        
        #continue to menu
        pygame.draw.rect(surface, COLOUR_TWO, continue_button)
        back_text = font.render("Continue", True, BLACK)
        surface.blit(back_text, (WIDTH // 2 - back_text.get_width() // 2, HEIGHT // 1.5 + 8))

        #toggle board view
        pygame.draw.rect(surface, COLOUR_TWO, toggle_button)
        toggle_text = font.render("View Board", True, BLACK)
        surface.blit(toggle_text, (WIDTH // 2 - toggle_text.get_width() // 2, HEIGHT // 1.33 + 8))
