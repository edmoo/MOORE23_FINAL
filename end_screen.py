import pygame
from const import *

#create the login button
continue_button = pygame.Rect(WIDTH // 4, HEIGHT // 1.5, WIDTH // 2, 32)
toggle_button = pygame.Rect(WIDTH // 4, HEIGHT // 1.33, WIDTH //2, 32)

#create the username and password fields
stats_field = pygame.Rect(WIDTH // 4, HEIGHT // 2, WIDTH // 2, 32)
title_font = pygame.font.SysFont("Oswald", 120)



class EndScreen:

    def __init__(self):
        pass

    #show methods

    def show_screen(self, surface, board, numTurns, toggleBoard):

        #clear surface
        surface.fill(COLOUR_ONE)

        result = board.result
        if result == "1-0":
            victor_text = title_font.render("WHITE WINS!", True, COLOUR_TWO)
        elif result == "0-1":
            victor_text = title_font.render("BLACK WINS!", True, COLOUR_TWO)
        else:
            victor_text = title_font.render("DRAW!", True, COLOUR_TWO)

        surface.blit(victor_text, ((WIDTH // 2)-victor_text.get_width()//2, HEIGHT // 3 + 8))
        
        #display number of turns taken
        pygame.draw.rect(surface, COLOUR_TWO, stats_field)
        statText = font.render("No. Turns: "+str(numTurns), True, BLACK)
        stat_text_pos = statText.get_rect(center=stats_field.center)
        surface.blit(statText, stat_text_pos)    

    
        #continue to menu
        pygame.draw.rect(surface, COLOUR_TWO, continue_button)
        back_text = font.render("1.Continue", True, BLACK)
        back_text_pos = back_text.get_rect(center=continue_button.center)
        surface.blit(back_text, back_text_pos)

        #toggle board view
        pygame.draw.rect(surface, COLOUR_TWO, toggle_button)
        toggle_text = font.render("2.View Board", True, BLACK)
        toggle_text_pos = toggle_text.get_rect(center=toggle_button.center)
        surface.blit(toggle_text, toggle_text_pos)
